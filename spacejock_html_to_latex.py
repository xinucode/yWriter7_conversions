#File for turning html book files into latex files

import time as timmy
import sys, os
import shutil
import unnest
import yaml
import pylatex
import story_parser as sp

class_loc = "reviseme_format\\diazessay.cls"
class_loc2 = "reviseme_format\\unnumberedtotoc.sty"

class spacejock_html_to_latex:
    def __init__(self,proj_file,auth_file):
        yamlfile = open(auth_file,"r")
        author_info = yaml.load(yamlfile, Loader=yaml.FullLoader)
        self.author = author_info["author"]
        self.street_address = author_info["street_address"]
        self.postal_code = author_info["postal_code"]
        self.email = author_info["email"]
        self.author_surname = author_info["author_surname"]
        yamlfile.close()

        yamlfile = open(proj_file,"r")
        project_info = yaml.load(yamlfile, Loader=yaml.FullLoader)
        self.DirectoryName = project_info['project_directory']
        self.file_stub = project_info['file_stub']
        self.title = project_info['title']
        if project_info['chapter_titles'] == 'None':
            self.chapters = False
        else:
            self.chapters = True
        if project_info['image_filename'] == 'None':
            self.image = None
        else:
            self.image = project_info['image_filename']
        yamlfile.close()
        
        self.story_contents = sp.story_parser( self.html_filename )
        # self.story_contents.story_preview()
        
    @property
    def html_filename(self):
        return os.path.join(self.DirectoryName,self.file_stub+".html")
        
    @property
    def tex_filename(self):
        return os.path.join(self.DirectoryName,self.file_stub)
        
    @property
    def tex_filename_full(self):
        return os.path.join(self.DirectoryName,self.file_stub+".tex")
        
    @property
    def class_dependencies(self):
        return os.path.join(self.DirectoryName,"diazessay.cls"),os.path.join(self.DirectoryName,"unnumberedtotoc.sty")
        
    def generate_latex(self):
    
        if os.path.isfile(class_loc):
            shutil.copy( class_loc, self.DirectoryName )
            shutil.copy( class_loc2, self.DirectoryName )
        else:
            print( "Class file chosen is not there" )
    
        doc = pylatex.Document(documentclass="diazessay",document_options="12")

        # set up libraries and commands
        doc.preamble.append(pylatex.Command('usepackage', "xcolor,soul,unnumberedtotoc"))
        doc.preamble.append(pylatex.utils.NoEscape(r'\newcommand{\threestars}{\begin{center}$ {\ast}\,{\ast}\,{\ast} $\end{center}}'))

        #set up preamble
        if self.image:
            doc.preamble.append(pylatex.utils.NoEscape(f"\\title{{\\includegraphics[width=0.5\\textwidth]{{{self.image}}}~\\\\[1cm]{self.title}}}"))
        else:
            doc.preamble.append(pylatex.Command('title', self.title))
        doc.preamble.append(pylatex.Command('author', self.author))
        doc.preamble.append(pylatex.Command('date', pylatex.utils.NoEscape(r'\today')))

        # set up title page
        doc.append(pylatex.Command('pagenumbering', "gobble"))
        doc.append(pylatex.utils.NoEscape(r'\maketitle'))
        doc.append(pylatex.Command('pagenumbering', "arabic"))
        if self.chapters:
            doc.append(pylatex.utils.NoEscape(r'\tableofcontents'))
        doc.append(pylatex.utils.NoEscape(r'\newpage'))

        
        for chap in self.story_contents.chapters.keys():
            if self.chapters:
            # print(chap)
                doc.append(pylatex.Command('addsec', chap.strip()))
            for scene in self.story_contents.chapters[chap]:
                for para in scene:
                    content = pylatex.utils.NoEscape(para.paragraph_to_tex())
                    if(content.strip()):
                        doc.append(content)
                    else:
                        doc.append(pylatex.utils.NoEscape(r'\bigskip'))
                    
                doc.append(pylatex.utils.NoEscape(r'\bigskip'))
                doc.append(pylatex.utils.NoEscape(r'\threestars'))
                doc.append(pylatex.utils.NoEscape(r'\bigskip'))
                
        doc.generate_tex(self.tex_filename)
        
if __name__=="__main__":
    this_proj = spacejock_html_to_latex("project_config.yml","author_config.yml")
    this_proj.story_contents.story_preview()
    this_proj.generate_latex()