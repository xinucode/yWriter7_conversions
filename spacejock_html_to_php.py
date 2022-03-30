#File for turning html book files into php files

import time as timmy
import sys, os
import shutil
import unnest
import yaml
import story_parser as sp

chars = set('0123456789$,abcdefghijklmnopqrstuvwxyz.ABCDEFGHIJKLMNOPQRSTUVWXYZ')
image_indicator = "##image##"
title_indicator = "##title##"
next_page_indicator = "##next_page##"
prev_page_indicator = "##prev_page##"
this_page_indicator = "##this_page##"
this_page_num_indicator = "##this_page_number##"
total_page_indicator = "##total_pages##"
paragraph_indicators = ["<p class='Para' id='##para_ref##'>","</p>"]
reference_indicator = "##para_ref##"

class spacejock_html_to_php:
    def __init__(self,infile):
        try:
            #retrieve info from config file
            yamlfile = open(infile,"r")
            project_info = yaml.load(yamlfile, Loader=yaml.FullLoader)
            self.BookDirectoryName = project_info['project_directory']
            self.SiteDirectoryName = project_info['outfile_directory']
            self.file_stub = project_info['file_stub']
            self.print_title = project_info['title']
            if project_info['image_filename'] == 'None':
                self.image = None
            else:
                self.image = project_info['image_filename']
            if project_info['chapter_titles'] == 'None' or project_info['chapter_titles'] == 'False' or project_info['chapter_titles'] == False:
                self.chapters = False
            else:
                self.chapters = True
        except KeyError as err:
            print("ERROR: missing key",err, "in", proj_file, "in php converter")
        finally:
            yamlfile.close()
        
        #create story object
        self.story_contents = sp.story_parser( self.html_filename )
        
        self.total_pages_by_scene = 0
        for chap in self.story_contents.chapters.keys():
            self.total_pages_by_scene=self.total_pages_by_scene+len(self.story_contents.chapters[chap])
        
    @property
    def html_filename(self):
        return os.path.join(self.BookDirectoryName,self.file_stub+".html")
        
    def php_filenames(self,index):
        return os.path.join(self.SiteDirectoryName,self.file_stub+"_p"+str(index)+".php")
        
    @property
    def dependencies(self):
        return os.path.join(self.SiteDirectoryName,"light_white_blue_red.png"),os.path.join(self.SiteDirectoryName,"dark_black_blue_red.png")
        
    def copy_over_dependencies(self):
        if self.image:
            image_path = os.path.join(self.BookDirectoryName,self.image)
            image_future_path = os.path.join(self.SiteDirectoryName,self.image)
            if os.path.isfile(image_future_path):
                print(f"Image already exists in destination.")
            elif os.path.isfile(image_path):
                shutil.copy( image_path, self.SiteDirectoryName )
            else:
                print("Cannot find image file:",image_path)
                
        files_to_copy = ["light_white_blue_red.png","dark_black_blue_red.png"]
        for file in files_to_copy:
            if os.path.isfile(file) and not os.path.isfile(os.path.join(self.SiteDirectoryName,file)):
                shutil.copy(file,self.SiteDirectoryName)
            elif not os.path.isfile(file):
                print(f"Cannot find file: {file}")
            elif os.path.isfile(os.path.join(self.SiteDirectoryName,file)):
                print(f"File {file} already exists in destination.")
        
    def generate_php_by_scene(self):
        self.copy_over_dependencies()
    
        page_num = 0 
        indicators = { "image_tag":'<img src="##image##" alt="##title##" class="cover-image">', "image":image_indicator, \
            "title_tag":'<h1 class="title"><b>##title##</b></h1>', "next_link":next_page_indicator, "prev_link":prev_page_indicator, \
            "chap_tag":"<p class='chapter'><b>Chapter 1</b></p>", "cover_image":'div class="cover-image">', "this_page":this_page_indicator, \
            "total_pages":total_page_indicator,"this_page_no":this_page_num_indicator,"subtitle_tag":'<h2 class="title"><b>##title##</b></h2>', \
            "title":title_indicator}
        
        # total_pages = 0
        # for chap in self.story_contents.chapters.keys():
            # total_pages=total_pages+len(self.story_contents.chapters[chap])
        
        for chap in self.story_contents.chapters.keys():
            for scene in self.story_contents.chapters[chap]:
            
                # phpfile = open( self.SiteDirectoryName+"\\"+self.file_stub+"_p"+str(page_num)+".php" , "w+" )
                phpfile = open( self.php_filenames(page_num) , "w+" )
                    #set up links
                replacements = { "image_tag":'<img src="##image##" alt="##title##" class="cover-image">', "image":self.image, \
                    "title_tag":'<h1 class="title"><b>##title##</b></h1>', "next_link":self.file_stub+"_p"+str(page_num+1)+".php", "prev_link":"", \
                    "chap_tag":"<p class='chapter'><b>Chapter: "+chap+"</b></p>", "cover_image":'div class="cover-image">', \
                    "this_page":self.file_stub+"_p"+str(page_num)+".php", "total_pages":str(self.total_pages_by_scene+1),"this_page_no":str(page_num+1), \
                    "subtitle_tag":'<h2 class="title"><b>##title##</b></h2>', "title":self.print_title}
                if self.image is None:
                    replacements["image_tag"] = ""
                    replacements["image"] = ""
                
                if( not self.chapters ):
                    replacements["chap_tag"] = ""
                
                if( page_num>=1 ):
                    replacements["prev_link"] = self.file_stub+"_p"+str(page_num-1)+".php"
                    #+f" page {page_num}"
                    replacements["title_tag"] = ""
                    # replacements["chap_tag"]+=f" Page {page_num+1}"
                    replacements["image_tag"] = ""
                    replacements["image"] = ""
                else:
                    replacements["subtitle_tag"] = ""
            
                #read and replace tags in header with story specific things
                header = open( "header.php", "r")
                line = "k"
                while line:
                    line = header.readline()
                    # print(line)
                    for i in indicators.keys():
                        if indicators[i] in line:
                            line = line.replace( indicators[i], replacements[i] )
                            
                    # line = line + "\n"
                    phpfile.write( line )
                header.close()
                
                for i,para in enumerate(scene):
                    phpfile.write( paragraph_indicators[0]+para.paragraph_to_html()+paragraph_indicators[1])
                
                phpfile.write("</font>\n")
                
                #insert footer onto page
                footer = open( "footer.php", "r")
                line = "k"
                while line:
                    line = footer.readline()
                    for i in indicators.keys():
                        if indicators[i] in line:
                            line = line.replace( indicators[i], replacements[i] )
                    # line = line + "\n"
                    phpfile.write( line )
                footer.close()
                
                page_num = page_num+1

                phpfile.close()
                
        #closing page
        phpfile = open( self.SiteDirectoryName+"\\"+self.file_stub+"_p"+str(page_num)+".php" , "w+" )
        #set up links
        #indicators = [image_indicator, title_indicator, next_page_indicator, prev_page_indicator, "<p class='chapter'><b>Chapter 1</b></p>", 'div class="cover-image">', this_page_indicator]
        replacements = { "image_tag":'<img src="##image##" alt="##title##" class="cover-image">', "image":self.image, \
            "title_tag":'<h1 class="title"><b>##title##</b></h1>', "next_link":"", "prev_link":self.file_stub+"_p"+str(page_num-1)+".php", \
            "chap_tag":"", "cover_image":'div class="final-image">',  "this_page":self.file_stub+"_p"+str(page_num)+".php", "total_pages":str(self.total_pages_by_scene+1), \
            "this_page_no":str(self.total_pages_by_scene+1), "subtitle_tag":"", "title":"Thanks for reading "+self.print_title+"!"}
        if self.image is None:
            replacements["image_tag"] = ""
            replacements["image"] = ""

        #read and replace tags in header with story specific things
        header = open( "header.php", "r")
        line = "k"
        while line:
            line = header.readline()
            for i in indicators.keys():
                if indicators[i] in line:
                    line = line.replace( indicators[i], replacements[i] )
            # line = line + "\n"
            phpfile.write( line )
        header.close()

        phpfile.write("</font>\n")
        
        
        #insert footer onto page
        footer = open( "footer.php", "r")
        line = "k"
        while line:
            line = footer.readline()
            for i in indicators.keys():
                if indicators[i] in line:
                    line = line.replace( indicators[i], replacements[i] )
            # line = line + "\n"
            phpfile.write( line )
        footer.close()

        phpfile.close()
        
if __name__=="__main__":
    this_proj = spacejock_html_to_php("project_config.yml")
    this_proj.story_contents.story_preview()
    this_proj.generate_php_by_scene() 