import spacejock_html_to_php as php
import spacejock_html_to_latex as tex
import spacejock_html_to_shunn as rtf
import argparse
import os

#parse arguments
parser = argparse.ArgumentParser(description="Define conversion types to run.")
parser.add_argument('-a','--author', type=str, help="path to author config file")
parser.add_argument('-p','--project', type=str, help="path to project config file")
parser.add_argument('--shunn', action='store_true', help="converts given project into a shunn formatted rtf document")
parser.add_argument('--tex', action='store_true', help="converts given project into a latex document")
parser.add_argument('--php', action='store_true', help="converts given project into a set of php reader files")
parser.add_argument('--all', action='store_true', help="runs all conversions")
parser.add_argument('-c','--clean', action='store_true', help="deletes all files produced by this program for this project")

#check inputs
if not parser.parse_args().author:
    print("WARNING: No author config filepath declared, using local author config file 'author_config.yml'.")
    author_config_file = 'author_config.yml'
else:
    author_config_file = parser.parse_args().author
    
if not parser.parse_args().project:
    print("WARNING: No project config filepath declared, using local project config file 'project_config.yml'.")
    project_config_file = 'project_config.yml'
else:
    project_config_file = parser.parse_args().project
    
#run conversion(s)
previewed = False
if parser.parse_args().shunn or parser.parse_args().all:
    try:
        shunn_output = rtf.spacejock_html_to_shunn(project_config_file,author_config_file)
        if not previewed:
            shunn_output.story_contents.story_preview()
            previewed = True
        shunn_output.generate_shunn()
        print("SUCCESS: shunn formatting complete")
    except:
        print("ERROR: Something went wrong with Shunn output")
    
if parser.parse_args().tex or parser.parse_args().all:
    try:
        latex_output = tex.spacejock_html_to_latex(project_config_file,author_config_file)
        if not previewed:
            latex_output.story_contents.story_preview()
            previewed = True
        latex_output.generate_latex()
        print("SUCCESS: latex formatting complete")
    except:
        print("ERROR: Something went wrong with latex output")
    
if parser.parse_args().php or parser.parse_args().all:
    try:
        php_output = php.spacejock_html_to_php(project_config_file)
        if not previewed:
            php_output.story_contents.story_preview()
            previewed = True
        php_output.generate_php_by_scene() 
        print("SUCCESS: php formatting complete")
    except:
        print("ERROR: Something went wrong with php output")
 
if parser.parse_args().clean:
    #clean up shunn files
    try:
        shunn_output = rtf.spacejock_html_to_shunn(project_config_file,author_config_file)
        if os.path.isfile(shunn_output.rtf_filename):
            os.remove(shunn_output.rtf_filename)
        print("SUCCESS: shunn cleanup complete")
    except:
        print("ERROR: Something went wrong with removing rtf file")
        
    #clean up latex files
    try:
        latex_output = tex.spacejock_html_to_latex(project_config_file,author_config_file)
        if os.path.isfile(latex_output.tex_filename_full):
            os.remove(latex_output.tex_filename_full)
        for item in latex_output.class_dependencies:
            if os.path.isfile(item):
                os.remove(item)
        print("SUCCESS: latex cleanup complete")
    except:
        print("ERROR: Something went wrong with removing latex file and dependencies")
        
    #clean up php files
    try:
        php_output = php.spacejock_html_to_php(project_config_file)
        for i in range( php_output.total_pages_by_scene+1 ):
            if os.path.isfile(php_output.php_filenames(i)):
                os.remove(php_output.php_filenames(i))
        for item in php_output.dependencies:
            if os.path.isfile(item):
                os.remove(item)
        print("SUCCESS: php cleanup complete")
    except:
        print("ERROR: Something went wrong with removing php files and dependencies")
        