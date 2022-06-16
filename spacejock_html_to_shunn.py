import sys, os
import yaml
import story_parser as sp

#file structure
#doc_header
#chapter_header
#para_header
#para text
#para_footer
#...
#para_header
#para text
#para_footer
#chapter_header
#para_header
#para text
#para_footer
#...
#doc_footer

center_command = "\\pard \\ltrpar\\s15\\qc \\fi720\\li0\\ri0\\sl-480\\slmult0\\nowidctlpar\\noline"



class spacejock_html_to_shunn:
    def __init__(self,proj_file,auth_file):
        try:
            yamlfile = open(auth_file,"r")
            author_info = yaml.load(yamlfile, Loader=yaml.FullLoader)
            self.author = author_info["author"]
            self.street_address = author_info["street_address"]
            self.postal_code = author_info["postal_code"]
            self.email = author_info["email"]
            self.author_surname = author_info["author_surname"]
        except KeyError as err:
            print("ERROR: missing key",err, "in", auth_file, "in shunn converter")
        finally:
            yamlfile.close()

        try:
            yamlfile = open(proj_file,"r")
            project_info = yaml.load(yamlfile, Loader=yaml.FullLoader)
            self.infiledir = project_info['project_directory']
            self.file_stub = project_info['file_stub']
            self.title = project_info['title']
            if project_info['chapter_titles'] == 'None' or project_info['chapter_titles'] == 'False' or project_info['chapter_titles'] == False:
                self.chapters = False
            else:
                self.chapters = True
            self.word_count = str(project_info['word_count'])
            self.book_type = project_info['book_type']
            if self.book_type!="short" and self.book_type!="novel":
                self.book_type="short"
            self.title_keyword = project_info['title_keyword']
        except KeyError as err:
            print("ERROR: missing key",err, "in", proj_file, "in shunn converter")
        finally:
            yamlfile.close()
        
        self.story_contents = sp.story_parser( self.html_filename )
        # self.story_contents.story_preview()
        
    @property
    def html_filename(self):
        return os.path.join(self.infiledir,self.file_stub+".html")
        
    @property
    def rtf_filename(self):
        return os.path.join(self.infiledir,self.file_stub+"_"+self.author_surname+".rtf")
        
    def generate_shunn(self):
        if self.book_type=="novel":
                            #times new roman rtf header (original was courier new; As a coder, a style that I like, but aparently not for everyone. Especially publishers)
            header_files = ["format-word\\doc_header_TNR.txt","format-word\\doc_footer.txt","format-word\\chapter_header.txt","format-word\\para_header.txt","format-word\\para_footer.txt"]
        else:
            header_files = ["format-word\\doc_header2_TNR.txt","format-word\\doc_footer2.txt","","format-word\\para_header2.txt","format-word\\para_footer.txt"]

        f0 = open( header_files[0], "r" )
        f2 = open( header_files[1], "r" )
        if self.book_type=="novel":
            f3 = open( header_files[2], "r" )
        f5 = open( header_files[3], "r" )
        f6 = open( header_files[4], "r" )
        doc_header = f0.read()
        doc_footer = f2.read()
        if self.book_type=="novel":
            chapter_header = f3.read()
        para_header = f5.read()
        para_footer = f6.read()
        f0.close()
        f2.close()
        if self.book_type=="novel":
            f3.close()
        f5.close()
        f6.close()
        
        scenebreak = False
        
        #open rtf file
        shunnfile = open( self.rtf_filename, "w+" )

        #write header
        doc_header = doc_header.replace( "Title Keyword", self.title_keyword )
        doc_header = doc_header.replace( "Author Byline", self.author )
        doc_header = doc_header.replace( "Author Name", self.author )
        doc_header = doc_header.replace( "Street Address", self.street_address )
        doc_header = doc_header.replace( "City and Postal Code", self.postal_code )
        doc_header = doc_header.replace( "Email Address", self.email )
        doc_header = doc_header.replace( "Author Surname", self.author_surname )
        if self.book_type=="novel":
            doc_header = doc_header.replace( "Novel Title", self.title )
        else:
            doc_header = doc_header.replace( "Story Title", self.title )
        if self.book_type=="novel":
            doc_header = doc_header.replace( "1,000", self.word_count )
        else:
            doc_header = doc_header.replace( "#666", self.word_count )
        shunnfile.write(doc_header)
        
        for chapter_index,chap in enumerate(self.story_contents.chapters.keys()):
            #write chapter header
            if self.book_type=="novel":
                if "Chapter" in chap:
                    curr_chapter_header = chapter_header.replace( "Chapter Title", "" ).replace( "#", str(chapter_index+1) )
                else:
                    curr_chapter_header = chapter_header.replace( "Chapter Title", chap ).replace( "#", str(chapter_index+1) )
                shunnfile.write(curr_chapter_header)
                
            final_scene = len(self.story_contents.chapters[chap])-1
            for i,scene in enumerate(self.story_contents.chapters[chap]):
                for para in scene:
                    shunnfile.write(para_header)
                    shunnfile.write(para.paragraph_to_rtf())
                    shunnfile.write(para_footer)
                if i<final_scene:
                    shunnfile.write(para_header)
                    shunnfile.write(para_footer)
                    # shunnfile.write(para_header)
                    shunnfile.write("{\\pard\\qc #\\par}")
                    # shunnfile.write(para_footer)
                    shunnfile.write(para_header)
                    shunnfile.write(para_footer)
        shunnfile.write(para_header)
        shunnfile.write(para_footer)
        shunnfile.write("{\\pard\\qc [END]\\par}") #test
        shunnfile.write(doc_footer)
        shunnfile.close()
        
        print("A FRIENDLY REMINDER: The RTF file is verified to be compatable with Windows OpenOffice Writer V4.1.12 and Microsoft Office 365 Word Version 2204. For compatability with previous versions of Microsoft Word, open the RTF file in a recent Word program and select File>Info>Convert for a document that is compatable across all versions of Word.")
        
if __name__=="__main__":
    this_proj = spacejock_html_to_shunn("project_config.yml","author_config.yml")
    this_proj.story_contents.story_preview()
    this_proj.generate_shunn()