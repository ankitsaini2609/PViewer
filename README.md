# PViewer
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Twitter](https://img.shields.io/twitter/follow/d3afh3av3n?style=social)](https://twitter.com/d3afh3av3n)

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Project Setup](#project-setup)
* [Usage](#usage)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)


<!-- ABOUT THE PROJECT -->
## About The Project

PViewer is a tool which will be used to find the conflicting policies for a AWS IAM user.


### Built With
* [python3](https://docs.python.org/3/)



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.


### Installation via pip

1. Install using pip:
```sh
pip3 install pviewer
```
2. Set the AWS_PROFILE as environment variable
```sh
export AWS_PROFILE=default
```
3. Run
```sh
python3 -m pviewer -u username
```


### Project Setup

1. Clone this repo
   * With HTTPS
   ```sh
   git clone https://github.com/ankitsaini2609/PViewer.git
   ```
   * With SSH (just use HTTPS if you aren't sure what SSH is)
   ```sh
   git clone git@github.com:ankitsaini2609/PViewer.git
   ```
2. Hop into the project directory
```sh
cd PViewer/pviewer
```
3. Install python3 packages
```sh
sudo pip3 install -r requirements.txt
```
4. Set the AWS_PROFILE as environment variable
```sh
export AWS_PROFILE=default
```
5. Run it :rocket:
```sh
python3 __main__.py -u username
```
Where username is IAM username in AWS for which you have to find the overlapping policies.\
6. Output\
![OUTPUT](https://github.com/ankitsaini2609/PViewer/blob/master/pviewer/output.png "output")


<!-- USAGE EXAMPLES -->
## Usage
Two policies allowing you to write objects in the same S3 bucket. It will plot a graph and connecting overlapping policies as edges.

![DEMO](https://github.com/ankitsaini2609/PViewer/blob/master/pviewer/demo.gif "demo")


<!-- LICENSE -->
## License

Distributed under the MIT License. See [LICENSE](https://github.com/ankitsaini2609/PViewer/blob/master/LICENSE.txt) for more information.



<!-- CONTACT -->
## Contact

Ankit Saini 
* Twitter - [@d3afh3av3n](https://twitter.com/d3afh3av3n)
* Github - [ankitsaini2609](https://github.com/ankitsaini2609)
* Medium - [ankitsaini2609](https://medium.com/@ankitsaini2609)
* LinkedIn - [ankitsaini2609](https://linkedin.com/in/ankitsaini2609)


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Choose an Open Source License](https://choosealicense.com)
