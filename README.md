# spacejock_conversions
Converts output html files into php, latex, and rtf outputs. 

Still in development phase but working.

These scripts take the html file produced by SpaceJock's yWriter7 output html file and converts it to several formats of my preference and need. 

## dependencies ##

SpaceJock's story writing software:
http://www.spacejock.com/yWriter.html

### python ###
These will probably be necessary for running these scripts.

* sys
* os
* yaml
* time
* shutil
* pylatex (only latex conversions)
* argparse

### html to rtf ###
The rtf file produced is in the shunn manuscript format required for submission to most publishes with a few personal touches. 

Example run:
```
	python spacejock_html_to_shunn.py
```
or 
```
	python run_conversions.py --shunn
```
To ensure maximum compatibility, I suggest to open the resulting file in Microsoft Word and select File>Info>Compatibility so that it works across all Microsoft Word office programs

### html to latex ###
This process produces a tex file and copies over dependencies to the project directory. The resulting tex file will need to be converted using a latex compiler. This file assumes you have installed the following libraries:
* fontenc
* inputenc
* lmodern
* textcomp
* lastpage
* xcolor
* soul

Example run:
```
	python spacejock_html_to_latex.py
```
or 
```
	python run_conversions.py --tex
```
### html to php ###
In order to read the php files, you will need some sort of php compiler. I have only tested this on Apache, but I assume others will work fine.

In order to make the reader more dyslexic friendly, you may need to install the font OpenDyslexic, available for free https://opendyslexic.org/.

Example run:
```
	python spacejock_html_to_php.py
```
or 
```
	python run_conversions.py --php
```

## Usage ##
### Setup ###
Before you run, you will need to set up two config files. One for authorship and one with the project details.

Example author config file:
```
author: "Sarah Skinner"
street_address: "1492 Nunyabiznis Ave"
postal_code: "Pittsburgh, PA 15217"
email: "sssm8d@gmail.com"
author_surname: "Skinner"
```

Example project config file:
```
title: Lorem Ipsum
file_stub: Lorem
project_directory: example\
cover_image_filename: Cosmic-Microwave-Background-Radiation.jpg
image_filename: pexels-ann-zzz-8452844.jpg
edit_mode: False
title_keyword: Lorem
chapter_titles: None
word_count: "1,000"
book_type: "short"
outfile_directory: example\
```

If none are specified the local config files will be ran. 

### Running ###
the main program can run the three different conversions and the arguments are described here:
```
usage: run_conversion.py [-h] [-a AUTHOR] [-p PROJECT] [--shunn] [--tex] [--php] [--all] [-c]

Define conversion types to run.

optional arguments:
  -h, --help            show this help message and exit
  -a AUTHOR, --author AUTHOR
                        path to author config file
  -p PROJECT, --project PROJECT
                        path to project config file
  --shunn               converts given project into a shunn formatted rtf document
  --tex                 converts given project into a latex document
  --php                 converts given project into a set of php reader files
  --all                 runs all conversions
  -c, --clean           deletes all files produced by this program for this project
```