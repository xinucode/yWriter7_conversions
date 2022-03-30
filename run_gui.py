import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
import os
from subprocess import run
import yaml

options = {'padx': 3, 'pady': 4}
title_options = {'padx': 5, 'pady': 7}
entry_width = 40
gui = tk.Tk()
gui.title('SpaceJock yWriter7 Conversions')
gui.geometry('600x650')
gui.iconbitmap('MeLogo3-purple-circle2.ico')

yes_all = tk.IntVar()
yes_rtf = tk.IntVar()
yes_tex = tk.IntVar()
yes_php = tk.IntVar()

author_path_tk = tk.StringVar()
author_path_tk.set("author_config.yml")

def open_file(frame,index,this_file,ftype = "p",initial_directory = "\\"):
    dialog_options = {}
    dialog_options['initialdir'] = os.path.realpath(initial_directory)
    file = filedialog.askopenfile(mode='r', filetypes=[('Config Files', '*.yml')], title="Select Config File",**dialog_options)
    if file:
        filepath = os.path.abspath(file.name)
        filelabel = ttk.Label(frame, text=str(filepath),wraplength=400)
        filelabel.grid(column=2, row=index, sticky='W', **options)
        this_file[0] = str(filepath)
    else:
        this_file = [""]
    if ftype == "a":
        author_path_tk.set(this_file[0])
      
def open_dir(frame,index,this_file):
   file = filedialog.askdirectory(initialdir=os.getcwd(), title="Select Project Directory")
   if file:
      filepath = os.path.abspath(file)
      filelabel = ttk.Label(frame, text=str(filepath),wraplength=300)
      filelabel.grid(column=1, row=index, sticky='W', **options)
      this_file[0] = str(filepath)
   else:
      this_file = [""]
      
def update_label(Filestub,message):
    if Filestub:
        message.set(f"Save to config/{Filestub}.yml")
    else:
        message.set("Save to config/{Filestub}.yml")
   
def convert(auth_file, proj_file, yall, rtf, tex, php):
    command = "python run_conversion.py -q"
    if auth_file:
        command += f" -a {auth_file[0]}"
    if proj_file:
        command += f" -p {proj_file[0]}"
    if yall or (rtf and tex and php):
        command+=" --all"
    else:
        if rtf:
            command+=" --shunn"
        if tex:
            command+=" --tex"
        if php:
            command+=" --php"
    print(command)
    errgui = tk.Tk()
    errgui.title('Terminal Output')
    errgui.geometry('600x500')
    errgui.iconbitmap('MeLogo3-purple-circle2.ico')
    output = run(command, capture_output=True).stdout
    command_output = ttk.Label(errgui, text=command,wraplength=450)
    command_output.grid(column=1,row=3, sticky='W',**options)
    run_output = ttk.Label(errgui, text=output,wraplength=450)
    run_output.grid(column=1,row=4, sticky='W',**options)
    
   
def save_to_yml(tit,stub,proD,imag,titkey,chaptit,count,stype,pout,folder = 'configs',run_conv = False):
    # config_settings = [ title, filestub, projdir, image, titlekey, chaptit, wordcount, storytype, php_outdir]
    if not tit or not stub or not proD:
        if not tit:
            error_message = "ERROR: Must have a 'Title' for project."
        elif not stub:
            error_message = "ERROR: Must have a 'Filestub'."
        else:
            error_message = "ERROR: Must have a 'Project Directory'."
            
        errgui = tk.Tk()
        errgui.title('Error Message')
        errgui.geometry('600x200')
        errgui.iconbitmap('MeLogo3-purple-circle2.ico')
        command_output = ttk.Label(errgui, text=error_message,wraplength=450)
        command_output.grid(column=0,row=0,**options)
    else:
        yml_items = [f'title: "{tit}"',f'file_stub: "{stub}"',f'project_directory: {proD}']
        if not imag:
            yml_items.append('image_filename: None')
        else:
            yml_items.append(f'image_filename: "{imag}"')
        if not stype:
            yml_items.append('book_type: False')
        else:
            yml_items.append(f'book_type: "{stype}"')
        if not chaptit:
            yml_items.append('chapter_titles: False')
        else:
            yml_items.append('chapter_titles: True')
        if not count:
            yml_items.append('word_count: "0"')
        else:
            yml_items.append(f'word_count: "{count}"')
        if not titkey:
            yml_items.append('title_keyword: False')
        else:
            yml_items.append(f'title_keyword: "{titkey}"')
        if not pout:
            yml_items.append(f'outfile_directory: {proD}')
        else:
            yml_items.append(f'outfile_directory: {pout}')
        
        output = "\n".join(yml_items)
        
        if not os.path.isdir(folder):
            os.mkdir(folder)
        yml_output = yaml.load(output, Loader=yaml.FullLoader)
        proj_path = os.path.join(folder,stub+".yml")
        with open( proj_path,'w+') as file:
            yaml.dump(yml_output, file)
            
            if not run_conv:
                succgui = tk.Tk()
                succgui.title('Success Message')
                succgui.geometry('600x200')
                succgui.iconbitmap('MeLogo3-purple-circle2.ico')
                command_output = ttk.Label(succgui, text=f"SUCCESS: Saved to {stub}.yml",wraplength=450)
                command_output.grid(column=0,row=0,**options)
            
        if run_conv:
            convert([author_path_tk.get()], [proj_path], yes_all.get(), yes_rtf.get(), yes_tex.get(), yes_php.get())
    
def author_window():
    form_gui = tk.Tk()
    form_gui.title('Author Config')
    form_gui.geometry('600x300')
    form_gui.iconbitmap('MeLogo3-purple-circle2.ico')
    form_frame1 = ttk.Frame(form_gui)
    author_name = tk.StringVar(form_gui)
    author_street = tk.StringVar(form_gui)
    author_postal = tk.StringVar(form_gui)
    author_email = tk.StringVar(form_gui)
    author_surname = tk.StringVar(form_gui)
    author_form(form_frame1,author_name,author_street,author_postal,author_email,author_surname)
    
    
def author_form(form_frame,author_name,author_street,author_postal,author_email,author_surname):
    form_frame.grid(column=0,row=0,padx=5, pady=5, sticky='W')
    author_label = ttk.Label( form_frame, text="Author Name:")
    author_label.grid(column=0,row=0,padx=5, pady=5, sticky='W')
    author_entry = tk.Entry(form_frame, width=entry_width, textvariable=author_name)
    author_entry.grid(column=1,row=0,padx=5, pady=5, sticky='W')
    
    street_label = ttk.Label( form_frame, text="House Number and Street:")
    street_label.grid(column=0,row=1,padx=5, pady=5, sticky='W') 
    street_entry = tk.Entry(form_frame, width=entry_width, textvariable=author_street)
    street_entry.grid(column=1,row=1,padx=5, pady=5, sticky='W')
    
    postal_label = ttk.Label( form_frame, text="City, State Postal Code:")
    postal_label.grid(column=0,row=2,padx=5, pady=5, sticky='W')
    postal_entry = tk.Entry(form_frame, width=entry_width, textvariable=author_postal)
    postal_entry.grid(column=1,row=2,padx=5, pady=5, sticky='W')
    
    email_label = ttk.Label( form_frame, text="Email:")
    email_label.grid(column=0,row=3,padx=5, pady=5, sticky='W')
    email_entry = tk.Entry(form_frame, width=entry_width, textvariable=author_email)
    email_entry.grid(column=1,row=3,padx=5, pady=5, sticky='W')
    
    surname_label = ttk.Label( form_frame, text="Surname or Short Name:")
    surname_label.grid(column=0,row=4,padx=5, pady=5, sticky='W')
    surname_entry = tk.Entry(form_frame, width=entry_width, textvariable=author_surname)
    surname_entry.grid(column=1,row=4,padx=5, pady=5, sticky='W')
    
    if len(author_path_tk.get())>30:
        author_path = "..."+author_path_tk.get()[-30:]
    else:
        author_path = author_path_tk.get()
    
    load_button = ttk.Button(form_frame, text=f'Load data from {author_path}', command=lambda : load_author_settings(form_frame,author_name,author_street,author_postal,author_email,author_surname))
    load_button.grid(column=1,row=5,padx=5, pady=5, sticky='W')
    clear_button = ttk.Button(form_frame, text='Clear Form', command=lambda : clear_form(form_frame,author_name,author_street,author_postal,author_email,author_surname))
    clear_button.grid(column=1,row=6,padx=5, pady=5, sticky='W')
    save_button = ttk.Button(form_frame, text=f'Save to {author_path}', command=lambda : save_author_settings( author_name,author_street,author_postal,author_email,author_surname))
    save_button.grid(column=1,row=7,padx=5, pady=5, sticky='W')
    
def clear_form(frame,author_name,author_street,author_postal,author_email,author_surname):
    author_name.set("")
    author_street.set("")
    author_postal.set("")
    author_email.set("")
    author_surname.set("")
    author_form( frame,author_name,author_street,author_postal,author_email,author_surname)
    
def load_author_settings( frame ,author_name,author_street,author_postal,author_email,author_surname):
    yamlfile = open(author_path_tk.get(),"r")
    
    try:
        project_info = yaml.load(yamlfile, Loader=yaml.FullLoader)
        author_name.set(project_info["author"])
        author_street.set(project_info["street_address"])
        author_postal.set(project_info["postal_code"])
        author_email.set(project_info["email"])
        author_surname.set(project_info["author_surname"])
    except Exception:
        errgui = tk.Tk()
        errgui.title('Error Message')
        errgui.geometry('600x200')
        errgui.iconbitmap('MeLogo3-purple-circle2.ico')
        command_output = ttk.Label(errgui, text="This is not an Author Config file",wraplength=450)
        command_output.grid(column=0,row=0,**options)
    
    author_form( frame,author_name,author_street,author_postal,author_email,author_surname)
    
def save_author_settings( author_name,author_street,author_postal,author_email,author_surname):
    if not author_name.get() or not author_street.get() or not author_postal.get() or not author_email.get() or not author_surname.get():
        errgui = tk.Tk()
        errgui.title('Error Message')
        errgui.geometry('600x200')
        command_output = ttk.Label(errgui, text="Missing fields",wraplength=450)
        command_output.grid(column=0,row=0,**options)
    else:
        output = f"""author: {author_name.get()}
street_address: {author_street.get()}
postal_code: {author_postal.get()}
email: {author_email.get()}
author_surname: {author_surname.get()}
"""
        yml_output = yaml.load(output, Loader=yaml.FullLoader)
        with open( author_path_tk.get(),'w+') as file:
            yaml.dump(yml_output, file)
            
            succgui = tk.Tk()
            succgui.title('Success Message')
            succgui.geometry('600x200')
            succgui.iconbitmap('MeLogo3-purple-circle2.ico')
            command_output = ttk.Label(succgui, text=f"SUCCESS: Saved to author_config.yml",wraplength=450)
            command_output.grid(column=0,row=0,**options)
      
def presets_form( presets_frame, config_list=[False, False, False, False, False, False, False, False, False]):
    # config_settings = [ title, filestub, projdir, image, titlekey, chaptit, wordcount, storytype, php_outdir]
    title = tk.StringVar()
    filestub = tk.StringVar()
    image = tk.StringVar()
    image.set("None")
    keyword = tk.StringVar()
    chap_tit = tk.IntVar()
    wordcount = tk.StringVar()
    booktype = tk.StringVar()
    proj_dir = [""]
    site_dir = [""]
    
    if config_list[0]:
        title.set(config_list[0])
        if config_list[1]:
            filestub.set(config_list[1])
        if config_list[2]:
            proj_dir[0] = config_list[2]
        if config_list[3]:
            image.set(config_list[3])
        if config_list[4]:
            keyword.set(config_list[4])
        if config_list[5]:
            chap_tit.set(1) 
        if config_list[6]:
            wordcount.set(config_list[6])
        if config_list[7]:
            booktype.set(config_list[7])
        if config_list[8]:
            site_dir[0] = config_list[8]
    
    save_message = tk.StringVar(value="Save to configs/{Filestub}.yml")
    #actual form
    #title
    title_label = ttk.Label(presets_frame, text="\tTitle:")
    title_label.grid(column=0, row=1, sticky='W', **options)
    title_entry = tk.Entry(presets_frame, width=entry_width, textvariable=title)
    title_entry.grid(column=1, row=1, sticky='W', **options)
    #filestub
    filestub_label = ttk.Label(presets_frame, text="\tFilestub:")
    filestub_label.grid(column=0, row=2, sticky='W', **options)
    filestub_entry = tk.Entry(presets_frame, width=entry_width, textvariable=filestub) #, command=update_label(filestub.get(),save_message), command=update_label(mini_frame3,filestub.get())
    filestub_entry.grid(column=1, row=2, sticky='W', **options)
    #project directory
    projdir_label = ttk.Label(presets_frame, text="\tProject Directory:")
    projdir_label.grid(column=0, row=3, sticky='W', **options)
    mini_frame0 = tk.Frame(presets_frame)
    projdir_entry = ttk.Button(mini_frame0, text='Browse', command=lambda : open_dir(mini_frame0,0,proj_dir))
    projdir_entry.grid(column=0, row=0, sticky='W', **options)
    projdir_load = ttk.Label(mini_frame0, text=proj_dir[0],wraplength=300, width=300)
    projdir_load.grid(column=1, row=0, sticky='W', **options)
    mini_frame0.grid(column=1, row=3, sticky='W', **options)
    #image
    image_label = ttk.Label(presets_frame, text="\tImage File:")
    image_label.grid(column=0, row=4, sticky='W', **options)
    image_entry = tk.Entry(presets_frame, width=entry_width, textvariable=image)
    image_entry.grid(column=1, row=4, sticky='W', **options)
    #title keyword
    keyword_label = ttk.Label(presets_frame, text="\tTitle Keyword:")
    keyword_label.grid(column=0, row=5, sticky='W', **options)
    keyword_entry = tk.Entry(presets_frame, width=entry_width, textvariable=keyword)
    keyword_entry.grid(column=1, row=5, sticky='W', **options)
    #chapter titles
    chap_tit_label = ttk.Label(presets_frame, text="\tChapter Titles:")
    chap_tit_label.grid(column=0, row=6, sticky='W', **options)
    chap_tit_entry = tk.Checkbutton(presets_frame, variable=chap_tit, onvalue=1, offvalue=0)
    chap_tit_entry.grid(column=1, row=6, sticky='W', **options)
    #wordcount
    wordcount_label = ttk.Label(presets_frame, text="\tWord Count:")
    wordcount_label.grid(column=0, row=7, sticky='W', **options)
    wordcount_entry = tk.Entry(presets_frame, width=entry_width, textvariable=wordcount)
    wordcount_entry.grid(column=1, row=7, sticky='W', **options)
    #booktype
    booktype_label = ttk.Label(presets_frame, text="\tStory Type:")
    booktype_label.grid(column=0, row=8, sticky='W', **options)
    mini_frame1 = tk.Frame(presets_frame)
    story_type_option1 = tk.Radiobutton( mini_frame1, text="Short", variable=booktype, value="short", indicator = 0)
    story_type_option1.grid(column=0, row=0, sticky='W', **options)
    story_type_option2 = tk.Radiobutton( mini_frame1, text="Novel", variable=booktype, value="novel", indicator = 0)
    story_type_option2.grid(column=1, row=0, sticky='W', **options)
    mini_frame1.grid(column=1, row=8, sticky='W', **options)
    #outfile directory
    outfile_label = ttk.Label(presets_frame, text="\tPHP Outfiles Directory:")
    outfile_label.grid(column=0, row=9, sticky='W', **options)
    mini_frame2 = tk.Frame(presets_frame)
    outfile_entry = ttk.Button(mini_frame2, text='Browse', command=lambda : open_dir(mini_frame2,0,site_dir))
    outfile_entry.grid(column=0, row=0, sticky='W', **options)
    outfile_load = ttk.Label(mini_frame2, text=site_dir[0],wraplength=300, width=300)
    outfile_load.grid(column=1, row=0, sticky='W', **options)
    mini_frame2.grid(column=1, row=9, sticky='W', **options)
    
    #buttons at the bottom
    mini_frame3 = tk.Frame(presets_frame)
    save_presets_label = ttk.Label(mini_frame3, textvariable=save_message, width=300)
    save_presets_label.grid(column=1, row=0, sticky='W', **options)
    save_presets_button = ttk.Button(mini_frame3, text="Save Form", command=lambda : save_to_yml(title.get(),filestub.get(), proj_dir[0],image.get(),keyword.get(),chap_tit.get(),wordcount.get(),booktype.get(),site_dir[0]))
    save_presets_button.grid(column=0, row=0, **options)
    mini_frame3.grid(column=1, row=10, sticky='W', **options)
    clear_button = ttk.Button(presets_frame,text="Clear Form", command=lambda : presets_form(presets_frame))
    clear_button.grid(column=0, row=10, **options)
    
    #author modify and run
    author_mod_button = ttk.Button(presets_frame,text="Modify Author Config", command=lambda : author_window())
    author_mod_button.grid(column=0, row=11, **options)
    run_button = ttk.Button(presets_frame,text="Run Conversions", command=lambda : save_to_yml(title.get(),filestub.get(), proj_dir[0],image.get(),keyword.get(),chap_tit.get(),wordcount.get(),booktype.get(),site_dir[0],'temp',True))
    run_button.grid(column=1, row=11, sticky='W', **options)
    
    # print(config_list)
    
    gui.mainloop()
      
def import_settings(import_file, config_settings, frame):
    # config_settings = [ title, filestub, projdir, image, titlekey, chaptit, wordcount, storytype, php_outdir]
    try:
        #retrieve info from config file
        yamlfile = open(import_file,"r")
        project_info = yaml.load(yamlfile, Loader=yaml.FullLoader)
        projdir = project_info['project_directory']
        sitedir = project_info['outfile_directory']
        filestub = project_info['file_stub']
        title = project_info['title']
        if project_info['image_filename'] == 'None':
            image = None
        else:
            image = project_info['image_filename']
        if project_info['chapter_titles'] == 'None' or project_info['chapter_titles'] == 'False' or project_info['chapter_titles'] == False:
            chaptit = False
        else:
            chaptit = True
        wordcount = str(project_info['word_count'])
        btype = project_info['book_type']
        if btype!="short" and btype!="novel":
            btype="short"
        key = project_info['title_keyword']
        config_settings[0] = title
        config_settings[1] = filestub
        config_settings[2] = projdir
        config_settings[3] = image
        config_settings[4] = key
        config_settings[5] = chaptit
        config_settings[6] = wordcount
        config_settings[7] = btype
        config_settings[8] = sitedir
        presets_form( frame, config_settings)
    except KeyError as err:
        errgui = tk.Tk()
        errgui.title('Error Message')
        errgui.geometry('600x200')
        errgui.iconbitmap('MeLogo3-purple-circle2.ico')
        command_output = ttk.Label(errgui, text="ERROR: missing key "+str(err)+" in "+import_file,wraplength=450)
        command_output.grid(column=0,row=0,**options)
    except Exception as err:
        errgui = tk.Tk()
        errgui.title('Error Message')
        errgui.geometry('600x200')
        command_output = ttk.Label(errgui, text="ERROR: "+str(err),wraplength=450)
        command_output.grid(column=0,row=0,**options)
    finally:
        yamlfile.close()
    
def load_file(frame):
    dialog_options = {}
    dialog_options['initialdir'] = os.path.realpath("configs")
    file = filedialog.askopenfile(mode='r', filetypes=[('Config Files', '*.yml')], title="Select Config File",**dialog_options)
    if file:
        filepath = os.path.abspath(file.name)
        configs = [False, False, False, False, False, False, False, False, False]
        import_settings(filepath,configs,frame)
    
      



selection_frame = ttk.Frame(gui)
frame = ttk.Frame(gui)
# scrollwindow = ttk.Frame(gui)
terminal_frame = ttk.Frame(gui)
presets_frame = ttk.Frame(gui)

choose_label = ttk.Label(selection_frame, text="Select Conversions:")
choose_label.grid(column=0, row=0, sticky='W', **options)

run_all_checkbox = tk.Checkbutton(selection_frame, text='All', variable=yes_all, onvalue=1, offvalue=0)
run_all_checkbox.grid(column=1, row=0, sticky='W', **options)
run_shunn_checkbox = tk.Checkbutton(selection_frame, text='Shunn(rtf)', variable=yes_rtf, onvalue=1, offvalue=0)
run_shunn_checkbox.grid(column=2, row=0, sticky='W', **options)
run_latex_checkbox = tk.Checkbutton(selection_frame, text='Latex(tex)', variable=yes_tex, onvalue=1, offvalue=0)
run_latex_checkbox.grid(column=3, row=0, sticky='W', **options)
run_php_checkbox = tk.Checkbutton(selection_frame, text='EReader(php)', variable=yes_php, onvalue=1, offvalue=0)
run_php_checkbox.grid(column=4, row=0, sticky='W', **options)

#option 1: enter filepath of config files setup like in the readme
option1 = ttk.Label(frame, text="Enter project config files:")
option1.grid(column=0, row=3, sticky='W', **title_options)
project_path_label = ttk.Label(frame, text='\tProject File:')
project_path_label.grid(column=0, row=4, sticky='W', **options)
project_path = ["project_config.yml"]
filelabel = ttk.Label(frame, text="Default: "+project_path[0],wraplength=400)
filelabel.grid(column=2, row=4, sticky='W', **options)
project_path_button = ttk.Button(frame, text='Browse', command=lambda : open_file(frame,4,project_path))
project_path_button.grid(column=1, row=4, **options)
author_path_label = ttk.Label(frame, text='\tAuthor File:')
author_path_label.grid(column=0, row=5, sticky='W', **options)
author_path = [author_path_tk.get()]
filelabel = ttk.Label(frame, text="Default: "+author_path[0],wraplength=400)
filelabel.grid(column=2, row=5, sticky='W', **options)
author_path_button = ttk.Button(frame, text='Browse', command=lambda : open_file(frame,5,author_path,"a"))
author_path_button.grid(column=1, row=5, **options)
outputs = ["",""]
run_with_paths_button = ttk.Button(frame, text='Run Conversions', command=lambda : convert(author_path,project_path,yes_all.get(),yes_rtf.get(),yes_tex.get(),yes_php.get()))
run_with_paths_button.grid(column=0, row=6, **options)
configs = [False, False, False, False, False, False, False, False, False]


#option 2: enter presets
option2 = ttk.Label(presets_frame, text="Or enter fields:")
option2.grid(column=0, row=0, sticky='W', **title_options)

mini_frame4 = tk.Frame(presets_frame)
load_presets_button = ttk.Button(mini_frame4, text='Load Story Settings From {Project File}', command=lambda : import_settings(project_path[0],configs,presets_frame))
load_presets_button.grid(column=1, row=0, sticky='W', **options)
load_config_file = ttk.Button(mini_frame4, text='Load Story Settings From Configs', command=lambda : load_file(presets_frame))
load_config_file.grid(column=0, row=0, sticky='W', **options)
mini_frame4.grid(column=1, row=0, sticky='W', **options)

selection_frame.grid(column=0,row=0,padx=5,pady=5, sticky='W')
frame.grid(column=0,row=1,padx=5, pady=5, sticky='W')
presets_frame.grid(column=0,row=2,padx=5,pady=5, sticky='W')
terminal_frame.grid(column=0,row=3,padx=5, pady=5, sticky='W')

presets_form( presets_frame, configs)

