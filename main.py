import ttkbootstrap
import os
import PIL.Image
from PIL.ExifTags import TAGS
from tkinter import *
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from datetime import datetime
import shutil

# Variables
themeName = "darkly"
output_folder = "../"
input_folder = "../"
file_list = []
photo_list = []

def getdata(path):
    image = PIL.Image.open(path)
    exifdata = image.getexif()
    for tag_id in exifdata:
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        if isinstance(data, bytes):
            data = data.decode()
        if(tag == "DateTime"):
            date_obj = datetime.strptime(data, '%Y:%m:%d %H:%M:%S')
            taken_date = date_obj.strftime("%Y:%m")
    return date_obj

def getInputfolderpath():
    global input_folder
    input_folder = filedialog.askdirectory()
    boxInputFolder.config(text= input_folder)
    getlistfiles(input_folder)

def getOutputfolderpath():
    global output_folder
    output_folder = filedialog.askdirectory()
    boxOutputFolder.config(text= output_folder)

def getlistfiles(path):
    global file_list
    global photo_list
    file_list = []
    photo_list = []
    file_list = os.listdir(path)
    for file in file_list:
        if(os.path.splitext(file)[1] == ".JPG" or os.path.splitext(file)[1] == ".PNG"):
            fileViewer.insert("", END, values=file)
            photo_list.append(file)


def movefile():
    year_file = os.listdir(output_folder)
    for photo in photo_list:
        src_path = input_folder + "/" + photo
        if getdata(src_path).strftime("%Y") in year_file:
            #print('year directory already exist')
            month_file = os.listdir(output_folder + "/" + getdata(src_path).strftime("%Y"))
            if getdata(src_path).strftime("%m") in month_file:
                #print('month directory already exist')
                shutil.copy(src_path,output_folder + "/" + getdata(src_path).strftime("%Y") + "/" + getdata(src_path).strftime("%m"))
            else:
                #print('month directory not exist')
                os.mkdir(output_folder + "/" + getdata(src_path).strftime("%Y") + "/" + getdata(src_path).strftime("%m"))
                shutil.copy(src_path,output_folder + "/" + getdata(src_path).strftime("%Y") + "/" + getdata(src_path).strftime("%m"))
        else:
            #print('year directory not exist')
            os.mkdir(output_folder + "/" + getdata(src_path).strftime("%Y"))
            os.mkdir(output_folder + "/" + getdata(src_path).strftime("%Y") + "/" + getdata(src_path).strftime("%m"))
            shutil.copy(src_path, output_folder + "/" + getdata(src_path).strftime("%Y") + "/" + getdata(src_path).strftime("%m")+ "/" + getdata(src_path).strftime('%Y:%m:%d-%Hh%Mm%Ss').replace(':', '_') + "-" + photo)

    Messagebox.show_info("Done")

def change_theme(name:str):
    global themeName
    themeName = name
    global style
    style(theme=name)

def sort():
    mb = Messagebox.yesno("Sort the pitures in : " + input_folder)
    if mb == "Oui":
        movefile()
    else:
        return


""" View """

# Set Theme
style = ttkbootstrap.Style
home = ttk.Window(themename=themeName)

# Set Tittle
home.title('Trieur De Photo - Crée par Lacroix Jérémy')

# Set window size
home.geometry("700x400")
home.grid_columnconfigure(tuple(range(8)), weight=1)

# Button Menu
BtnTheme = ttk.Menubutton(home, bootstyle="secondary",  text ="Select theme")
BtnTheme.menu = Menu(BtnTheme)
BtnTheme["menu"] = BtnTheme.menu
BtnTheme.menu.add_command(label="Dark", command=lambda :change_theme("darkly"))
BtnTheme.menu.add_command(label="Light", command=lambda :change_theme("cosmo"))

# Select FolderInput
LabelInputFolder = ttk.Label(text="Input folder")
boxInputFolder = ttk.Label(bootstyle="inverse", text=output_folder, width=20)
BtnFolderInput = ttk.Button(home, bootstyle="secondary", text ="Select folder", command =lambda :getInputfolderpath())

# Select FolderOutput
LabelOutputFolder = ttk.Label(text="Output folder")
boxOutputFolder = ttk.Label(bootstyle="inverse", text=input_folder, width=20)
BtnFolderOutput = ttk.Button(home, bootstyle="secondary", text ="Select folder", command =lambda :getOutputfolderpath())

# File visualization
columns = ("Name")
fileViewer = ttk.Treeview(bootstyle='secondary', columns=columns, show="headings")
fileViewer.heading("Name", text="Name")

# Button sort
BtnSort = ttk.Button(home, bootstyle="success",  text ="Sort", width=70, command= lambda :sort())

# --------- Grid System -------- #

# Menu
BtnTheme.grid(row = 0, column = 0, sticky = W)

# FolderInput
LabelInputFolder.grid(row=1, column=0, sticky=W, padx=20, pady=(20,2))
boxInputFolder.grid(row=2, column=0, sticky=W, padx=20)
BtnFolderInput.grid(row=3, column=0, sticky=E, padx=20, pady=(2,20))

# FolderOutput
LabelOutputFolder.grid(row=4, column=0, sticky=W, padx=20, pady=(20,2))
boxOutputFolder.grid(row=5, column=0, sticky=W, padx=20)
BtnFolderOutput.grid(row=6, column=0, sticky=E, padx=20, pady=(2,20))

# File visualization
fileViewer.grid(row=1, rowspan=6, column=1, columnspan=7, padx=10 ,sticky=NSEW)

# Button sort
BtnSort.grid(row=8,column=0,columnspan=7, pady=(70,70))

# Loop for real time
home.mainloop()

#print(getdata("BKPU9707.JPG"))