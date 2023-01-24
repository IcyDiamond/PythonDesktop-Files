from tkinter import *
import tkinter as tk
import os
import ctypes
import pathlib
import shutil

drives = [ chr(x) + ":" for x in range(65,91) if os.path.exists(chr(x) + ":") ]
# Increas Dots Per inch so it looks sharper
ctypes.windll.shcore.SetProcessDpiAwareness(True)

root = tk.Tk()
# set a title for our file explorer main window
root.title('Simple Explorer')
root.geometry("1200x550")
menu = Menu(root, tearoff = 0)
emptypastebin = "PasteBin Empty"

def this_pc():
    if currentPath.get() == "This PC":
        filelist.delete(0, END)
        for drive in drives:
            filelist.insert('end',f"{drive}\\")
    return

class Path:
    def __init__(self):
        #old = None
        data = None

    
    def search(self,event,*args):
        try:
            directory = os.listdir(currentPath.get())
        finally:
            this_pc()
        val = event.widget.get()
        self.val = StringVar()
        if val == '':
            data = directory
        else:
            data=[]
            for item in directory:
                if val.lower() in item.lower():
                    data.append(item)

        self.pathChange(data=data)
        
    def pathChange(self,*event,data):
        # Get all Files and Folders from the given Directory
        this_pc()
        # Clearing the list
        filelist.delete(0, END)
        # Inserting the files and directories into the list
        for file in data:
            filelist.insert('end', file)

    def changePathByClick(self,event=None):
        # Get clicked item.
        picked = filelist.get(filelist.curselection()[0])
        # get the complete path by joining the current path with the picked item
        path = os.path.join(currentPath.get(), picked)
        # Check if item is file, then open it
        #old = currentPath.get()
        if os.path.isfile(path):
            print('Opening: '+path)
            os.startfile(path)
        # Set new path, will trigger pathChange function.
        else:
            #old = currentPath.get()
            #print("old",old)
            currentPath.set(path)
            #new = currentPath.get()
            #print("new",new)

        #Goes back
        #self.backhistory(old)
        #root.bind("<Button-5>", lambda x: self.backhistory(old))

    #def forwardhistory(self,old,event=None):
    #    new = currentPath.get()
    #    print("new",new)
    #    currentPath.set(path)
    #    print("old",old)
    #    #Goes back
    #    root.bind("<Button-5>", lambda x: self.backhistory(old))

    #def backhistory(self,old,event=None):
    #    print("old",old)
    #    new = currentPath.get()
    #    print("new",new)
    #    #Goes forwards
    #    root.bind("<Button-4>", lambda x: currentPath.set(old))
    #    self.forwardhistory()
    

    def goBack(self,event=None):
        # set it to currentPath
        old = currentPath.get()
        print(old)
        currentPath.set(pathlib.Path(currentPath.get()).parent)
        new = currentPath.get()
        print(new)
        filelist.delete(0, END)
        data = os.listdir(currentPath.get())
        for file in data:
            filelist.insert('end', file)
        self.pathChange(data=data)
        # simple message

        #Goes forwards
        #root.bind("<Button-5>", lambda x: currentPath.set(old))


path = Path()

def open_popup():
    global top
    top = Toplevel(root)
    top.geometry("250x150")
    top.resizable(False, False)
    top.title("Child Window")
    top.columnconfigure(0, weight=1)
    Label(top, text='Enter File or Folder name').grid()
    Entry(top, textvariable=newFileName).grid(column=0, pady=10, sticky='NSEW')
    Button(top, text="Create", command=newFileOrFolder).grid(pady=10, sticky='NSEW')
    filelist.listBox.bind("<Button-3>", filelist.rightClick)

def newFileOrFolder():
    # check if it is a file name or a folder
    data = os.listdir(currentPath.get())
    if len(newFileName.get().split('.')) != 1:
        open(os.path.join(currentPath.get(), newFileName.get()), 'w').close()
    else:
        os.mkdir(os.path.join(currentPath.get(), newFileName.get()))
    # destroy the top
    top.destroy()
    path.pathChange(data=data)

top = ''

# String variables
newFileName = StringVar(root, "File.dot", 'new_name')
currentPath = StringVar(
    root,
    name='currentPath',
    value=pathlib.Path.cwd()
)
# Bind changes in this variable to the pathChange function
data = os.listdir(currentPath.get())
currentPath.trace('w', lambda x, y, z: path.pathChange(data=data))

Button(root, text='Folder Up', command=path.goBack).place(y=0,x=0, height=39)
Button(root, text='This PC', command= lambda: setThisPC()).place(x=0, y=39,width=100,height=39)
def setThisPC():
    currentPath.set("This PC")
    this_pc()
height=39
base=39+39
for drive in drives:
    height=height+39
    Button(root, text=(f"Drive: ({drive})"), command= lambda d=drive: currentPath.set(f"{d}\\")).place(x=0, y=height,width=100,height=39)

    Button(root, text=(f"Local Disk: ({drives[0]})"), command= lambda: currentPath.set(f"{drives[0]}\\")).place(x=0, y=base,width=100,height=39)

# Keyboard shortcut for going up

root.bind("<Alt-Up>", path.goBack)



Entry(root, textvariable=currentPath).place(x=62,y=0,height=39,width=10000)
# List of files and folder
filelist = Listbox(root)
filelist.place(x=100,y=39,height=510,width=10000)

class CutCopyPaste:
    def __init__(self):
        self.cut_path = None
        self.copy_path = None

    def get_selected_file_path(self):
        picked = filelist.get(filelist.curselection()[0])
        return os.path.join(currentPath.get(), picked)

    def reset_paths(self):
        self.cut_path = None
        self.copy_path = None
        
    def cut_action(self, event=None):
        self.reset_paths()
        self.cut_path = self.get_selected_file_path()
        emptypastebin = "paste"
        contextmenu(emptypastebin)
        
        print(f"Cut File: {self.cut_path}")

    def copy_action(self, event=None):
        self.reset_paths()
        self.copy_path = self.get_selected_file_path()
        emptypastebin = "copy"
        contextmenu(emptypastebin)
        
        print(f"Copy File: {self.copy_path}")

    def paste_action(self, event=None):
        if self.cut_path:
            print(f"Cut From: {self.cut_path}")
            path = currentPath.get()
            file_name = os.path.basename(self.cut_path)
            os.replace(self.cut_path, f"{path}\\{file_name}")
            print(f"Pasted to: {path}\\{file_name}")

            self.reset_paths()
            emptypastebin = "PasteBin Empty"
            contextmenu(emptypastebin)
            return

        if self.copy_path:
            print(f"Copy From: {self.copy_path}")
            path = currentPath.get()
            file_name = os.path.basename(self.copy_path)
            shutil.copy(self.copy_path, f"{path}\\{file_name}")
            print(f"Pasted to: {path}\\{file_name}")
            # Do paste stuff, but don't delete the file since it's a copy operation

            self.reset_paths()
            emptypastebin = "PasteBin Empty"
            contextmenu(emptypastebin)
            return
        
        emptypastebin = "PasteBin Empty"
        contextmenu(emptypastebin)
        


CutCopyPaste = CutCopyPaste()

# List Accelerators
filelist.bind('<Double-1>', path.changePathByClick)
filelist.bind('<Return>', path.changePathByClick)
filelist.bind('<<Cut>>', CutCopyPaste.cut_action)
filelist.bind('<<Copy>>', CutCopyPaste.copy_action)
filelist.bind('<<Paste>>', CutCopyPaste.paste_action)

# Menu
menubar = Menu(root)
# Adding a new File button
menubar.add_command(label="Add File or Folder", command=open_popup)
# Adding a quit button to the Menubar
menubar.add_command(label="Quit", command=root.quit)
# Make the menubar the Main Menu
root.config(menu=menubar)
# Call the function so the list displays
path.pathChange(data=data)
# run the main program
# define function to cut 
# the selected text
def cut_text():
    filelist.event_generate(("<<Cut>>"))
# define function to copy 
# the selected text
def copy_text():
        filelist.event_generate(("<<Copy>>"))
# define function to paste 
# the previously copied text
def paste_text():
    filelist.event_generate(("<<Paste>>"))
        
# create menubar
def contextmenu(emptypastebin):
    menu.delete(0,10)
    menu.add_command(label="Open", command=path.changePathByClick)
    menu.add_separator()
    menu.add_command(label="Cut", command=cut_text) 
    menu.add_command(label="Copy", command=copy_text)
    if emptypastebin == "PasteBin Empty":
        pass
    else:
        menu.add_command(label="Paste", command=paste_text)
    menu.add_separator()
    menu.add_command(label="Exit", command=root.destroy)
    return
# define function to popup the
# context menu on right button click 
def context_menu(event):
    try:
        if filelist.nearest(event.y) in filelist.curselection():
            pass
        else:
            filelist.select_clear(0, END)
            filelist.selection_set(filelist.nearest(event.y))
        filelist.activate(filelist.nearest(event.y))
        menu.tk_popup(event.x_root, event.y_root)
    finally: 
        menu.grab_release()

def ctrl(event):
    try:
        filelist.selection_set(filelist.nearest(event.y))
        filelist.activate(filelist.nearest(event.y))
    finally:
        filelist.selection_set(filelist.nearest(event.y))
        filelist.activate(filelist.nearest(event.y))

entry = Entry(root)
entry.place(y=0,x=1050, height=39)
entry.bind('<KeyRelease>', path.search)

if __name__ == "__main__":
    contextmenu(emptypastebin)
    root.bind("<Control-Button-1>", ctrl)
    root.bind("<Button-3>", context_menu)
    root.mainloop()