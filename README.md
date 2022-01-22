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

### html to rtf ###
The rtf file produced is in the shunn manuscript format required for submission to most publishes with a few personal touches. 

Example run:
```
	python spacejock_html_to_shunn.py
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
### html to php ###
In order to read the php files, you will need some sort of php compiler. I have only tested this on Apache, but I assume others will work fine.

In order to make the reader more dyslexic friendly, you may need to install the font OpenDyslexic, available for free https://opendyslexic.org/.

Example run:
```
	python spacejock_html_to_php.py
```
