# papermate
A Python package to help researchers and academics write papers using Markdown.

This package was first introduced as a blog post on [scientificallysound.org][blog].

## Requirements

While `papermate` does not have any Python dependencies, it does require some external dependencies.

- *pandoc*: Required
- *LaTeX*: Required for PDF output; [TexLive][tex] can be downloaded for all operating systems
- *git*: Required if want to render previous versions of document, or to render marked-up PDF showing difference between two version of document

## Installation

Download this repository.

You can install `papermate` system-wide or in a virtual environment. 

If you want to use `papermate` in a dedicated virtual environment, make sure you are in the `papermate` directory and run the following commands to create and activate a virtual environment:

```bash
$ cd papermate
$ python3 -m venv venv
$ source venv/bin/activate
(venv)$
```

Making sure you are in the top-most `papermate` directory (i.e. the one that contains `setup.py`), run the following command to install `papermate`:

```bash
$ pip install .
```

To verify that the package is installed properly, run the following command:

```bash
$ papermate -h
usage: papermate [-h] [--input INPUT] [--csl CSL] [--bib BIB] [-t] [-d] [--tags TAGS [TAGS ...]]

Papermate v0.1

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

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         Markdown file containing paper (e.g. paper.md)
  --csl CSL             csl style file to format bibliography (e.g. APA.csl)
  --bib BIB             .bib file containing references (e.g. refs.bib)
  -t, --tex             Output .tex verion of paper
  -d, --docx            Output .docx verion of paper
  --tags TAGS [TAGS ...]
                        Pair of git tags used to generate PDF diff document

```

You should see the help printed to your screen.

## First steps

With LaTeX install on your system, you can use `papermate` to render the tutorial PDF located in the `demo` folder.

First, we will change to the `demo` folder:

```bash
$ cd demo
$ ls -p
bib/  header.yaml  img/  paper.md  tex/
```

We can see that the `demo` directory contains a Markdown document, a YAML file, and a few directories.

Rendering the Markdown document to PDF can be done by running the `papermate` command on the command-line. If you created a virtual environment and install `papermate` within that virtual environment, you will have to activate the virtual environment before running the following command.

```bash
$ papermate
$ ls -p
bib/  header.yaml  img/  paper.md  paper.pdf  tex/
```

We can see that a new PDF document has been created. When no arguments are provided, papermate will look for a Markdown file in the current directory, and Citation Style Language and BibTeX reference files in a `bib` directory.

The more explicit way to achieve the same results would be to run:

```bash
$ papermate --input paper.md --csl bib/vancouver-author-date.csl --bib bib/refs.bib
```

## Next steps

Additional documentation will be added in the future. For now, please refer to the relevant [blog post][blog] on scientificallysound.org. 


[blog]: https://scientificallysound.org/2021/10/05/papermate-a-tool-for-academic-writers/
[tex]: https://tug.org/texlive/

