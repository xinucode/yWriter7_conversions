import html

test_file = "C:\\Users\\sarah\\Documents\\Sarah's Brain\\My Books and Ideas\\dark_stories\\short_stories\\Export\\the_mimic_v1.4.html"

##spacejock tags
heading_indicators = ["<p class='chapter'>","</p>"]
bold_indicators = ["<b>","</b>"]
italics_indicators = ["<i>","</i>"]
para_indicators = ["<p class='Para'>","</p>"]
scene_indicator = "<center></center>"
im_not_sure_about_this = "<p align='right'>"
all_indicators = heading_indicators+bold_indicators+italics_indicators+para_indicators+[scene_indicator]+[im_not_sure_about_this]

#xinuwrite tags
x_header_break = "######"
x_title_tag = "Title:"
x_project_tag = "Project:"
x_date_tag = "Date:"


def strip_indicators( line, indicators ):
    for item in indicators:
        line = line.replace(item, "")
        line = line.replace(item, "")
    return line
    
def remove_front_spaces( sentence ):
    if len(sentence)==0:
        return sentence
    if sentence[0]!=" ":
        return sentence
    if sentence[0]==" ":
        return remove_front_spaces(sentence[1:])
        
def remove_rear_spaces( sentence ):
    if len(sentence)==0:
        return sentence
    if sentence[-1]!=" ":
        return sentence
    if sentence[-1]==" ":
        return remove_rear_spaces(sentence[:-1])
        
def clean_up_line_latex( line):
#   line = line.replace("&hellip;", "...")
#   line = line.replace( "&#8220;", '"')
#   line = line.replace( "&#8221;", '"')
#   line = line.replace( "&#8217; ", "\\textquotesingle \ ")
#   line = line.replace( "&#8216; ", "\\textquotesingle \ ")
#   line = line.replace( "&#8217;", "\\textquotesingle ")
#   line = line.replace( "&#8216;", "\\textquotesingle ")
#   line = line.replace( "&#8230;", "...")
#   line = line.replace( "&#246;", "$\\ddot{\\textup{o}}$")
#   line = line.replace( "&#252;", "$\\ddot{\\textup{u}}$")
#   line = line.replace( "&#228;", "$\\ddot{\\textup{a}}$")
#   line = line.replace( "&#211;", "$\\acute{\\textup{O}}$")
#   line = line.replace( "&mdash;", "---")
#   line = line.replace( "&#8212;", "---")
#   line = line.replace( "&lt;", "<")
#   line = line.replace( "&gt;", ">")
#   line = line.replace( "&#239;", "$\\ddot{\\textup{\\i}}$")
#   #must be done last 
#   line = line.replace( "#", "\\#" )
  line = html.unescape(line)
  line = line.replace( "“", '"' )
  line = line.replace( "”", '"' )
  line = line.replace( "’", "'" )
#   line = line.replace( "’", "'" ) 
  return line
    
class story_text:
    def __init__( self, this_text, bold = False, italics = False):
        self.bold = bold
        self.italics = italics
        self.text = this_text
        
    def plain(self):
        for item in all_indicators:
            if item in self.text:
                return False
        return True
        
class story_paragraph:
    def __init__(self, this_text):
        self.contents = [story_text(this_text)]
        success = self.format_paragraph()
        while not success:
            success = self.format_paragraph()
            # self.paragraph_print()
        
    def format_paragraph( self ):
        new_format = None
        for i,text in enumerate(self.contents):
            if italics_indicators[0] in text.text:
                unitalics, yesitalics = text.text.split(italics_indicators[0],1)
                if unitalics and yesitalics:
                    text.text = unitalics
                    text.italics = False
                    new_format = story_text(yesitalics, italics = True, bold = text.bold)
                    break
                elif unitalics:
                    text.text = unitalics
                    text.italics = False
                elif yesitalics:
                    text.text = yesitalics
                    text.italics = True
            if italics_indicators[1] in text.text:
                yesitalics, unitalics = text.text.split(italics_indicators[1],1)
                if unitalics and yesitalics:
                    text.text = yesitalics
                    text.italics = True
                    new_format = story_text(unitalics, italics = False, bold = text.bold)
                    break
                elif unitalics:
                    text.text = unitalics
                    text.italics = False
                elif yesitalics:
                    text.text = yesitalics
                    text.italics = True
            if bold_indicators[0] in text.text:
                unbold, yesbold = text.text.split(bold_indicators[0],1)
                if unbold and yesbold:
                    text.text = unbold
                    text.bold = False
                    new_format = story_text(yesbold, bold = True, italics = text.italics)
                    break
                elif unbold:
                    text.text = unbold
                    text.bold = False
                elif yesbold:
                    text.text = yesbold
                    text.bold = True
            if bold_indicators[1] in text.text:
                yesbold, unbold = text.text.split(bold_indicators[1],1)
                if unbold and yesbold:
                    text.text = yesbold
                    text.bold = True
                    new_format = story_text(unbold, bold = False, italics = text.italics)
                    break
                elif unbold:
                    text.text = unbold
                    text.bold = False
                elif yesbold:
                    text.text = yesbold
                    text.bold = True
                
        if new_format:
            self.contents.insert(i+1,new_format)
            return False
        else:
            return True
    
    def paragraph_print(self):
        for text in self.contents:
            print("\t\t\tP: ",text.text, text.italics, text.bold)
            
    def paragraph_to_html(self):
        out_text = ""
        for text in self.contents:
            if text.italics and text.bold:
                out_text = out_text+bold_indicators[0]+italics_indicators[0]+text.text+italics_indicators[1]+bold_indicators[1]
            elif text.italics:
                out_text = out_text+italics_indicators[0]+text.text+italics_indicators[1]
            elif text.bold:
                out_text = out_text+bold_indicators[0]+text.text+bold_indicators[1]
            else:
                out_text = out_text+text.text
        if out_text.strip() == "":
            out_text = "<br>\n"
        return out_text
        
    def paragraph_to_rtf(self):
        rtf_italics_indicators = ["\\i ", "\\i0 "]
        rtf_bold_indicators = ["\\b ", "\\b0 "]
        out_text = ""
        for text in self.contents:
            if text.italics and text.bold:
                out_text = out_text+rtf_bold_indicators[0]+rtf_italics_indicators[0]+text.text+rtf_italics_indicators[1]+rtf_bold_indicators[1]
            elif text.italics:
                out_text = out_text+rtf_italics_indicators[0]+text.text+rtf_italics_indicators[1]
            elif text.bold:
                out_text = out_text+rtf_bold_indicators[0]+text.text+rtf_bold_indicators[1]
            else:
                out_text = out_text+text.text
                
        out_text = out_text.replace( "\n", "" )
#         out_text = out_text.replace( "&#8220;", '"')
#         out_text = out_text.replace( "&#8221;", '"')
#         out_text = out_text.replace( "&#8216;", "'")
#         out_text = out_text.replace( "&#8217;", "'")
#         out_text = out_text.replace( "&#8230;", "…")
#         out_text = out_text.replace( "&#246;", "ö")
#         out_text = out_text.replace( "&#252;", "ü")
#         out_text = out_text.replace( "&#228;", "ä")
#         out_text = out_text.replace( "&#211;", "Ó")
#         out_text = out_text.replace( "&mdash;", "—")
#         out_text = out_text.replace( "&#8212;", "—")
#         out_text = out_text.replace("&hellip;", "…")
#         out_text = out_text.replace( "&gt;", ">")
#         out_text = out_text.replace( "&#239;", "ï")
        
        out_text = html.unescape(out_text)
        
        out_text = remove_front_spaces(out_text)
        out_text = remove_rear_spaces(out_text)
        # if out_text.strip() == "":
            # out_text = "\n"
        return out_text
        
    def paragraph_to_tex(self):
        tex_italics_indicators = ["\\textit{", "}"]
        tex_bold_indicators = ["\\textbf{", "}"]
        out_text = ""
        for text in self.contents:
            if text.italics and text.bold:
                out_text = out_text+tex_bold_indicators[0]+tex_italics_indicators[0]+text.text+tex_italics_indicators[1]+tex_bold_indicators[1]
            elif text.italics:
                out_text = out_text+tex_italics_indicators[0]+text.text+tex_italics_indicators[1]
            elif text.bold:
                out_text = out_text+tex_bold_indicators[0]+text.text+tex_bold_indicators[1]
            else:
                out_text = out_text+text.text
                
        if "[" in out_text and "]" in out_text:
            out_text = out_text.replace( "[", "\\sethlcolor{red}\\hl{[")
            out_text = out_text.replace( "]", "]}" )
        return clean_up_line_latex(out_text)+"\n"

class story_parser:
    def __init__(self, file, file_type = "html"):
        if file_type=="html": #spacejock html output
            f = open(file, "r")
            self.chapters = {}
            line = f.readline()
            while line:
                if heading_indicators[0] in line:
                    this_chapter = strip_indicators( line, all_indicators)
                    self.chapters[this_chapter] = [[]]
                    this_scene = 0
                if para_indicators[0] in line:
                    line = strip_indicators( line, para_indicators)
                    line = strip_indicators( line, [im_not_sure_about_this])
                    if "%" in line:
                        line = line.replace( "%", " percent" )
                    self.chapters[this_chapter][this_scene].append(story_paragraph(line))
                if scene_indicator in line:
                    this_scene = this_scene+1
                    self.chapters[this_chapter].append([])
                line = f.readline()
            f.close()

            clean = False
            while not clean:
                clean = self.clean_final_breaks()
        elif file_type=="str": #xinuwrite entry file
            lines = file.split("\n")
            lines = [line.strip() for line in lines]
            title = ""
            project = ""
            date = ""
            header_index = 0
            for i,line in enumerate(lines):
                if line.startswith(x_title_tag):
                    title = line.replace(x_title_tag,"",1).strip()
                elif line.startswith(x_project_tag):
                    project = line.replace(x_project_tag,"",1).strip()
                elif line.startswith(x_date_tag):
                    date = line.replace(x_date_tag,"",1).strip()
                elif line==x_header_break:
                    header_index = i
            self.chapters = {project:[[]]}
                          #chap  #scene #first paragraph
            self.chapters[project][0].append(f"{title} {date}")
            for line in lines[header_index+1:]:
                if "%" in line:
                    self.chapters[project][0].append(story_paragraph(line.replace( "%", " percent" )))
                else:
                    self.chapters[project][0].append(story_paragraph(line))
        else:
            print("Bad filetype in story_parser")
        
    def clean_final_breaks( self):
        for chap in self.chapters.keys():
            if not self.chapters[chap][-1]:
                self.chapters[chap].pop()
        for chap in self.chapters.keys():
            for i,scene in enumerate(self.chapters[chap]):
                final_para = scene[-1]
                if len(final_para.contents)==1 and not final_para.contents[0].text.strip():
                    self.chapters[chap][i].pop()
                    return False
        return True
    
    def story_preview(self,full = False):
        for chapter in self.chapters.keys():
            print(chapter)
            for i,scene in enumerate(self.chapters[chapter]):
                print(f"\tscene {i}")
                count = len(scene)
                print(f"\t\t{count} paragraphs")
                if full:
                    for para in scene:
                        para.paragraph_print()
        

if __name__=="__main__":
    mimic = story_parser(test_file)
    mimic.story_preview(True)
    for chapter in mimic.chapters.keys():
        print(mimic.chapters[chapter][0][0].paragraph_to_html())
        break