from setuptools import setup

setup(
    name='papermate',
    version=0.1,
    author='Martin Heroux',
    packages=['papermate'],
    entry_points={'console_scripts' : ['papermate = papermate.papermate:main']}
    )

