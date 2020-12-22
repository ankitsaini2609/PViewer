import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pviewer",
    version="1.0",
    description="pviewer is a tool which will be used to find the conflicting policies for a AWS IAM user",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ankitsaini2609/PViewer",
    author="Ankit Saini",
    author_email="ankitsaini2609@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["pviewer"],
    include_package_data=True,
    install_requires=["boto3", "graphviz", "pytest"],
    entry_points={
        "console_scripts": [
            "pviewer=pviewer.__main__:main",
        ]
    },
)