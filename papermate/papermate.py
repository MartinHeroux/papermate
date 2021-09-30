from argparse import ArgumentParser, HelpFormatter
from dataclasses import dataclass
from pathlib import Path
import textwrap
import os


@dataclass
class Files:
    md: Path
    csl: Path
    bib: Path


def main():
    args = parse_command_line()
    files = get_files(args)
    format = get_format(args)
    tags = args.tags
    make_paper(files, format, tags)

def parse_command_line():
    USAGE = """Papermate v0.1

    Created by Martin Héroux (heroux.martin at gmail.com)

    Render paper written in Markdown to either PDF, DOCX or TEX.

    Can output difference of two versions of the paper to PDF
    based on their git tags.

    To tag your current version in git, use the following command:
    $ git tag -a v1 -m 'First draft'
    Adjust version number and message as needed.

    To tag an earlier version, use the following command:
    $ git tag -a v2 <commit checksum>
    Where 'commit checksum' is the entire (or first part of)
    the commit checksum. This can be obtained using:

    $ git log --pretty=oneline

    USAGE:
                """
    parser = ArgumentParser(description=USAGE, formatter_class=RawFormatter)
    parser.add_argument(
        "--input",
        type=str,
        default=None,
        help="Markdown file containing paper (e.g. paper.md)",
    )
    parser.add_argument(
        "--csl",
        type=str,
        default=None,
        help="csl style file to format bibliography (e.g. APA.csl)",
    )
    parser.add_argument(
        "--bib",
        type=str,
        default=None,
        help=".bib file containing references (e.g. refs.bib)",
    )
    parser.add_argument(
        "-t",
        "--tex",
        action="store_true",
        help="Output .tex verion of paper",
    )
    parser.add_argument(
        "-d",
        "--docx",
        action="store_true",
        help="Output .docx verion of paper",
    )
    parser.add_argument(
        "--tags",
        nargs="+",
        default=None,
        help="Pair of git tags used to generate PDF diff document",
    )
    args = parser.parse_args()
    return args

def get_files(args):
    """Get .md, .csl and .bib files"""
    bib_directory = Path("bib")
    if args.input is None:
        md = list(Path(".").glob("*.md"))[0]
    else:
        md = Path(args.input)
    if args.csl is None:
        csl = list(bib_directory.glob("*.csl"))[0].name
        csl = bib_directory / csl
    else:
        csl = Path(args.csl)
    if args.bib is None:
        bib = list(bib_directory.glob("*.bib"))[0].name
        bib = bib_directory / bib
    else:
        bib = Path(args.bib)
    return Files(md, csl, bib)


def get_format(args):
    """Determine format of output file"""
    format = "pdf"
    if args.docx:
        format = "docx"
    if args.tex:
        format = "tex"
    return format


def make_paper(files, format, tags):
    if make_current_version(tags):
        pandoc(files, format)
    else:
        get_tagged_markdown(files.md, tags)
        pandoc(files, format, tags)
        if len(tags) == 2:
            make_pdf_diff(tags)
        cleanup(tags)


def make_current_version(tags):
    return tags is None


def pandoc(files, format, tags=None):
    """Run Pandoc on command line"""
    if tags and len(tags) == 2:
        format = "tex"
    filenames = get_pandoc_filenames(files, tags)
    for filename in filenames:
        pandoc_command = (
            f"pandoc {filename}.md "
            "--defaults=header.yaml "
            f"--csl={files.csl} "
            f"--bibliography={files.bib} "
            f"-o {filename}."
            f"{format}"
        )
        os.system(pandoc_command)


def get_pandoc_filenames(files, tags):
    filenames = list()
    if tags is None:
        filenames.append(files.md.stem)
    else:
        filenames = tags
    return filenames


def get_tagged_markdown(md_file, tags):
    "Retrieve git tagged version(s) of paper in markdown format"
    for tag in tags:
        git_command = f"git cat-file -p {tag}:" f"{md_file.name} > " f" {tag}.md"
        os.system(git_command)


def make_pdf_diff(tags):
    diff_filename = f"{tags[0]}_{tags[1]}_diff.tex"
    latex_diff_command = f"latexdiff {tags[0]}.tex {tags[1]}.tex > {diff_filename}"
    os.system(latex_diff_command)
    os.system(f"xelatex {diff_filename}")


def cleanup(tags):
    filenames = tags
    if len(tags) == 2:
        filenames.append("_".join([tags[0], tags[1], "diff"]))
    for filename in filenames:
        os.system(f"rm -f {filename}.md ")
        os.system(f"rm -f {filename}.tex ")
        os.system(f"rm -f {filename}.aux ")
        os.system(f"rm -f {filename}.log ")


class RawFormatter(HelpFormatter):
    def _fill_text(self, text, width, indent):
        text = textwrap.dedent(text)
        text = textwrap.indent(text, indent)
        text = text.splitlines()
        text = [textwrap.fill(line, width) for line in text]
        text = "\n".join(text)
        return text


if __name__ == "__main__":
    main()

