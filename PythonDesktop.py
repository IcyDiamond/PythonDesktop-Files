from screeninfo import get_monitors
from tkinter.constants import *
from PIL import Image, ImageTk
from tkinter import PhotoImage
from tkinter import messagebox
from threading import Thread
from Taskbar import Taskbar
import tkinter as tk
import subprocess
import signal
import atexit
import json
import time
import sys
import os

#threadlist = []
#threadlist.append(Thread(target=lambda: os.system('explorer.exe &')))
#threadlist.append(Thread(target=lambda: os.kill(os.getpid(), signal.SIGTERM)))

#def exit_handler():
#    for t in threadlist:
#        time.sleep(1)
#        t.start()
#
#    for t in threadlist:
#        time.sleep(1)
#        t.join()
    

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("300x400")
        self.title("Python Desktop")
        self.signin_frame = tk.Frame(self)
        self.signup_frame = tk.Frame(self)
        self.desktop_frame = tk.Frame(self)
        self.signin_frame.grid_propagate(0)
        self.signup_frame.grid_propagate(0)
        self.desktop_frame.grid_propagate(0)
        self.signin_screen = signin_screen(self)

class Variables:
    def __init__(self):
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.desktop_files = os.path.dirname(os.path.abspath(__file__))
        self.users = os.path.join(self.desktop_files, "users")
        self.file_explorer = os.path.join(self.desktop_files, "FileExplorer.py")
        self.desktop_list = f"{self.users}\\{Auth.username}\\desktop"
        self.icon_images = os.path.join(f"{self.desktop_files}\\Windows\\system32")

        self.monitors = get_monitors()
        for i in range(len(self.monitors)):
            if self.monitors[i].is_primary == False:
                pass
            else:
                self.monitor_width = self.monitors[i].width
                self.monitor_height = self.monitors[i].height
    
    def refresh_var(self):
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.desktop_files = os.path.dirname(os.path.abspath(__file__))
        self.users = os.path.join(self.desktop_files, "users")
        self.file_explorer = os.path.join(self.desktop_files, "FileExplorer.py")
        self.desktop_list = f"{self.users}\\{Auth.username}\\desktop"
        self.icon_images = os.path.join(f"{self.desktop_files}\\Windows\\system32")
        self.monitors = get_monitors()

        self.monitors = get_monitors()
        for i in range(len(self.monitors)):
            if self.monitors[i].is_primary == False:
                pass
            else:
                self.monitor_width = self.monitors[i].width
                self.monitor_height = self.monitors[i].height

class Auth:
    username = ""
    password = ""
    username_stored = ""
    username_input_value = True
    password_input_value = True
    username_stored_value = False
    confirm_password_input_value = True

#signin screen
class signin_screen:
    def __init__(self, master):
        self.master = master
        self.initialized = False
        self.initialize_obj()

    def initialize_obj(self):
        if not self.initialized:
            #places the signin frame
            self.master.signin_frame.pack()

            #clears any widgets
            for widgets in self.master.signup_frame.winfo_children():
                widgets.destroy()
            self.master.signup_frame.pack_forget()

            #makes all the input fields and signin button
            self.username_input = tk.Entry(self.master.signin_frame,bg="light gray",validate="key")
            self.password_input = tk.Entry(self.master.signin_frame,bg="light gray",validate="key")
            self.signin_button = tk.Button(self.master.signin_frame, width=16, text="SignIn", command=self.signin, bg="Green")
            self.link = tk.Label(self.master.signin_frame, text="Need an account? S\u0332I\u0332G\u0332N\u0332 \u0332U\u0332P\u0332",font=('Helveticabold', 8), cursor="hand2")

            #places the widgets onto the screen
            self.username_input.pack()
            self.password_input.pack()
            self.signin_button.pack()
            self.link.pack()

            #Fills the input fields
            Auth.password_input_value = True
            self.password_input.insert(0, "Password")

            #validates the charcters in the textbox
            self.username_input.configure(validatecommand=(self.master.register(self.validate), '%P'))
            self.password_input.configure(validatecommand=(self.master.register(self.validate), '%P'))

            #binds the buttons to a function
            self.link.bind("<Button-1>", lambda e:self.hyperlink())
            self.password_input.bind("<FocusIn>", self.password_text)
            self.username_input.bind("<FocusIn>", self.username_text)
            self.password_input.bind("<FocusOut>", self.password_out)
            self.username_input.bind("<FocusOut>", self.username_out)
            self.username_input.bind("<Return>", self.signin)
            self.password_input.bind("<Return>", self.signin)
            self.stored_check()
            self.initialized = True

    def validate(self, P):
        #only allow A-Z, a-z, 0-9, and common symbols
        return all(c.isalnum() or c in '!@#$%^&*()_-+=[]{}\\|;:\'",.<>?/' for c in P)

    #Check all the info in the inputs
    def signin(self, event=NONE):
        if any(field.get().isspace() or field.get() in ["Username",""] for field in (self.username_input, self.password_input)):
            messagebox.showerror("Error", "Field above can not be blank!")
            return
        
        if not os.path.exists(f"{variables.users}\\{self.username_input.get()}"):
            messagebox.showerror("Error", "Username or Password is incorrect!")
            return

        with open(f"{variables.users}\\{self.username_input.get()}\\credentials.json", "r") as file:
            credentials = json.load(file)

        if not self.password_input.get() == credentials["current_password"]:
            messagebox.showerror("Error", "Username or Password is incorrect!")
            return
            
        Auth.username = self.username_input.get()
        Auth.password = self.password_input.get()
        messagebox.showinfo("Success","signin successful!")
        self.username_input_value = True
        self.password_input_value = True
        self.desktop = Desktop_screen(self.master)
        self.desktop.initialize_obj()
    
    def stored_check(self):
        if Auth.username_stored_value == True:
            self.username_input.insert(0, Auth.username_stored)
            Auth.username_stored_value = False
        else:
            self.username_input.insert(0, "Username")
        
    def hyperlink(self):
        self.master.signin_frame.pack_forget()
        
        if self.username_input.get().isspace() or self.username_input.get() in ["Username",""]:
            Auth.username_input_value = True
        else:
            Auth.username_stored = self.username_input.get()
            Auth.username_stored_value = True

        Auth.password_input_value = True
        Auth.confirm_password_input_value = True

        self.signup_screen = Signup_screen(self.master)
        self.signup_screen.initialize_obj()
        
    #if the field is emtpy it puts the text "password"
    def password_out(self,e):
        if self.password_input.index("end") == 0 or  self.username_input.get().isspace():
            self.password_input.config(show="")
            self.password_input.insert(0, "Password")
            Auth.password_input_value = True

    #if the username is emtpy or just spaces
    def username_out(self,e):
        if self.username_input.index("end") == 0 or  self.username_input.get().isspace():
            self.username_input.insert(0, "Username")
            Auth.username_input_value = True

    #Clears text when password field is clicked
    def password_text(self,e):
        if Auth.password_input_value == True:
            self.password_input.config(show="*")
            self.password_input.delete(0, "end")
            Auth.password_input_value = False

    #keeps the username if the user filled out that field
    def username_text(self,e):
        if Auth.username_input_value == True:
            self.username_input.delete(0, "end")
            Auth.username_input_value = False

class Signup_screen():
    def __init__(self, master):
        self.master = master        

    def initialize_obj(self):
        self.master.signup_frame.pack()
        
        #clears any widgets
        for widgets in self.master.signin_frame.winfo_children():
            widgets.destroy()
        self.master.signin_frame.pack_forget()
        
        #makes all the input fields and signin button
        self.username_input = tk.Entry(self.master.signup_frame,bg="light gray",validate="key")
        self.password_input = tk.Entry(self.master.signup_frame,bg="light gray",validate="key")
        self.confirm_password_input = tk.Entry(self.master.signup_frame, bg="light gray",validate="key")
        self.signup_button = tk.Button(self.master.signup_frame, width=16, text="SignUp", command=self.signup, bg="Green")
        self.link = tk.Label(self.master.signup_frame, text="Already a User? S\u0332I\u0332G\u0332N\u0332 \u0332I\u0332N\u0332",font=('Helveticabold', 8), cursor="hand2")

        #places the widgets onto the screen
        self.username_input.pack()
        self.password_input.pack()
        self.confirm_password_input.pack()
        self.signup_button.pack()
        self.link.pack()

        #Fills the input fields
        self.password_input.insert(0, "Password")
        self.confirm_password_input.insert(0, "Confirm Password")

        self.username_input.configure(validatecommand=(self.master.register(self.validate), '%P'))
        self.password_input.configure(validatecommand=(self.master.register(self.validate), '%P'))
        self.confirm_password_input.configure(validatecommand=(self.master.register(self.validate), '%P'))

        #binds the buttons to a function
        self.link.bind("<Button-1>", lambda e:self.hyperlink())
        self.password_input.bind("<FocusIn>", self.password_text)
        self.username_input.bind("<FocusIn>", self.username_text)
        self.password_input.bind("<FocusOut>", self.password_out)
        self.username_input.bind("<FocusOut>", self.username_out)
        self.confirm_password_input.bind("<FocusIn>", self.confirm_password_text)
        self.confirm_password_input.bind("<FocusOut>", self.confirm_password_out)
        self.username_input.bind("<Return>", self.signup)
        self.password_input.bind("<Return>", self.signup)
        self.confirm_password_input.bind("<Return>", self.signup)
        self.stored_check()

    def validate(self, P):
        #only allow A-Z, a-z, 0-9, and common symbols
        return all(c.isalnum() or c in '!@#$%^&*()_-+=[]{}\\|;:\'",.<>?/' for c in P)

    def signup(self, event=None):
        Auth.username = self.username_input.get()
        Auth.password = self.password_input.get()

        if self.username_input.get().isspace() or self.username_input.get() in ["Username",""] or self.password_input.get().isspace() or self.password_input.get() in ["Password",""]:
            messagebox.showerror("Error", "Field above can not be blank!")
            return
            
        if not self.confirm_password_input.get() == self.password_input.get():
            messagebox.showerror("Error", "Passwords dont match")
            return

        if os.path.exists(f"{variables.users}\\{Auth.username}"):
            messagebox.showerror("Error", "That user is already in use")
            return

        Auth.username_stored = self.username_input.get()
        Auth.username_stored_value = True

        data = {"current_password": self.password_input.get()}

        os.mkdir(f"{variables.users}\\{Auth.username}")
        with open(f"{variables.users}\\{Auth.username}\\credentials.json", "w") as file:
            json.dump(data, file)

        os.mkdir(f"{variables.users}\\{Auth.username}\\desktop")

        messagebox.showinfo("Success","signup successful!")
        self.master.signin_screen = signin_screen(self.master)

    def stored_check(self):
        if Auth.username_stored_value == True:
            self.username_input.insert(0, Auth.username_stored)
            Auth.username_stored_value = False
        else:
            self.username_input.insert(0, "Username")

    def hyperlink(self):
        self.master.signup_frame.pack_forget()

        if self.username_input.get().isspace() or self.username_input.get() in ["Username",""]:
            Auth.username_input_value = True
        else:
            Auth.username_stored = self.username_input.get()
            Auth.username_stored_value = True
        Auth.password_input_value = True
        Auth.confirm_password_input_value = True

        self.master.signin_screen = signin_screen(self.master)
        self.master.signin_screen.initialize_obj()

    #if the username is emtpy or just spaces
    def username_out(self,e):
        if self.username_input.index("end") == 0 or  self.username_input.get().isspace():
            self.username_input.insert(0, "Username")
            Auth.username_input_value = True

    #if the field is emtpy it puts the text "password"
    def password_out(self,e):
        if self.password_input.index("end") == 0 or  self.password_input.get().isspace():
            self.password_input.config(show="")
            self.password_input.insert(0, "Password")
            Auth.password_input_value = True

    def confirm_password_out(self,e):
        if self.confirm_password_input.index("end") == 0 or  self.confirm_password_input.get().isspace():
            self.confirm_password_input.configure(validatecommand=())
            self.confirm_password_input.config(show="")
            self.confirm_password_input.insert(0, "Confirm Password")
            self.confirm_password_input.configure(validatecommand=(self.master.register(self.validate), '%P'))
            Auth.confirm_password_input_value = True

    #keeps the username if the user filled out that field
    def username_text(self,e):
        if Auth.username_input_value == True:
            self.username_input.delete(0, "end")
            Auth.username_input_value = False

    #Clears text when password field is clicked
    def password_text(self,e):
        if Auth.password_input_value == True:
            self.password_input.config(show="*")
            self.password_input.delete(0, "end")
            Auth.password_input_value = False

    def confirm_password_text(self,e):
        if Auth.confirm_password_input_value == True:
            self.confirm_password_input.config(show="*")
            self.confirm_password_input.delete(0, "end")
            Auth.confirm_password_input_value = False

class Desktop_screen():
    def __init__(self, master):
        self.master = master
        self.img_ref = []
        self.text_ref = []
        self.icon_dict = {}
        self.view_icons_value = True
        self.grid=True
        self.new_folder_copy = 0
        self.menu_x = 0
        self.menu_y = 0
        self.show_start_menu = True
        self.side_bar_initialized = False
        self.side_bar_active = False
        self.start_menu = None
        self.image = None
        self.x = None
        self.y = None
        self.icon_id = 0
        self.monitor_height = variables.monitor_height
        
        self.max = 900
        self.size = 100
        self.height = 50
        self.add = 0

    def initialize_taskbar(self):
        self.new_window = tk.Toplevel(self.master)
        self.start = Taskbar(self.new_window)

    def initialize_obj(self):
        #clears any widgets
        for widgets in self.master.signin_frame.winfo_children():
            widgets.destroy()
        window.attributes('-fullscreen',True)
        self.master.signin_frame.pack_forget()
        self.master.signup_frame.pack_forget()
        self.master.desktop_frame.pack(fill=BOTH, expand=True)
        self.initialize_taskbar()

        #wallpaper
        self.icon_photo = PhotoImage(file=os.path.join(variables.icon_images, "UnknownIcon_Medium.png"))
        self.wallpaper = ImageTk.PhotoImage(Image.open(os.path.join(f"{variables.current_directory}\\Windows\\Web\\Wallpaper\\Wallpaper.jpg")))
        self.folders = ImageTk.PhotoImage(Image.open(os.path.join(variables.icon_images, "Folder_medium.png")))
        self.desktop = tk.Canvas(self.master.desktop_frame, bg="black", highlightthickness=0)
        self.desktop.pack(side=LEFT,fill=BOTH, expand=True)
        self.desktop.create_image(0, 0, image = self.wallpaper, anchor = NW)


        #icons
        initialized = False
        self.icon_size_var_set = 'medium'
        
        self.icon_size(self.max, self.size, self.height, self.add, initialized)
        
        #----------------------------------------Work in progress (context menu)--------------------------------------------------------------------

        #makes the right click menu on desktop
        self.desktop_menu = tk.Menu(self.master.desktop_frame, tearoff=0)
        self.icon_menu = tk.Menu(self.master.desktop_frame, tearoff=0)
        self.desktop_submenu = tk.Menu(self.master.desktop_frame, tearoff=0)

        #view sub menu
        self.view_icons_var = tk.BooleanVar()
        self.align_grid_var = tk.BooleanVar()
        self.icon_size_var = tk.StringVar()
        self.icon_size_var.set("medium")
        self.align_grid_var.set(True)
        self.view_icons_var.set(True)#                                                          max 600 for laptops
        self.desktop_submenu.add_radiobutton(label="Large icons", variable=self.icon_size_var,
                                             value="large", command=self.set_icon_size)
        self.desktop_submenu.add_radiobutton(label="Medium icons", variable=self.icon_size_var,
                                             value="medium", command=self.set_icon_size)
        self.desktop_submenu.add_radiobutton(label="Small icons", variable=self.icon_size_var,
                                             value="small", command=self.set_icon_size)
        self.desktop_submenu.add_separator()
        self.desktop_submenu.add_command(label="Auto Arrange icons")
        self.desktop_submenu.add_checkbutton(label="Align icons to grid", command=self.align_grid)
        self.desktop_submenu.add_separator()
        self.desktop_submenu.add_checkbutton(label="Show desktop icons", command=self.veiw_icons)
        self.desktop_submenu.entryconfigure("Align icons to grid",  variable=self.align_grid_var)
        self.desktop_submenu.entryconfigure("Show desktop icons",  variable=self.view_icons_var)

        #main menu
        self.desktop_menu.add_cascade(label='View', menu=self.desktop_submenu)
        self.desktop_menu.add_command(label="Sort by")
        self.desktop_menu.add_command(label="Refresh", command=self.place_icons)
        self.desktop_menu.add_separator()
        self.desktop_menu.add_command(label="Paste")
        self.desktop_menu.add_command(label="Paste shortcut")
        self.desktop_menu.add_separator()
        self.desktop_menu.add_command(label="New", command=self.new_folder)
        self.desktop_menu.add_separator()
        self.desktop_menu.add_command(label="Display Settings")
        self.desktop_menu.add_command(label="Personalize")


        #disabled menu options
        self.desktop_menu.entryconfig("View", state="normal")
        self.desktop_menu.entryconfig("Sort by", state="disabled")
        self.desktop_menu.entryconfig("Refresh", state="normal")

        self.desktop_menu.entryconfig("Paste", state="disabled")
        self.desktop_menu.entryconfig("Paste shortcut", state="disabled")

        self.desktop_menu.entryconfig("New", state="normal")

        self.desktop_menu.entryconfig("Display Settings", state="disabled")
        self.desktop_menu.entryconfig("Personalize", state="disabled")


        self.desktop_submenu.entryconfig("Large icons", state="normal")
        self.desktop_submenu.entryconfig("Medium icons", state="normal")
        self.desktop_submenu.entryconfig("Small icons", state="disabled")

        self.desktop_submenu.entryconfig("Auto Arrange icons", state="disabled")
        self.desktop_submenu.entryconfig("Align icons to grid", state="disabled")

        self.desktop_submenu.entryconfig("Show desktop icons",  state="disabled")

        self.desktop.bind("<Button-3>", self.do_popup)

        #---------------------------------------------------WIP folder context menus---------------------------------------------------

        self.icon_menu.add_command(label="Open")
        self.icon_menu.add_cascade(label="7-Zip")
        self.icon_menu.add_separator()
        self.icon_menu.add_cascade(label="Give access to")
        self.icon_menu.add_command(label="Restore previous versions")
        self.icon_menu.add_cascade(label="Include in libary")
        self.icon_menu.add_command(label="Pin to start")
        self.icon_menu.add_separator()
        self.icon_menu.add_cascade(label="Send to")
        self.icon_menu.add_separator()
        self.icon_menu.add_command(label="Cut")
        self.icon_menu.add_command(label="Copy")
        self.icon_menu.add_separator()
        self.icon_menu.add_command(label="Create shortcut")
        self.icon_menu.add_command(label="Delete")
        self.icon_menu.add_command(label="Rename")
        self.icon_menu.add_separator()
        self.icon_menu.add_command(label="Properties")

    def set_icon_size(self):
        # Get the selected icon size
        icon_size = self.icon_size_var.get()

        if icon_size == "large":
            self.icon_size(800, 140, 80, 10, False)
            self.icon_size_var_set = 'large'
        elif icon_size == "medium":
            self.icon_size(900, 100, 50, 0, False)
            self.icon_size_var_set = 'medium'
        elif icon_size == "small":
            self.icon_size(900, 50, 35, -10, False)
            self.icon_size_var_set = 'small'

    def new_folder(self):
        icon_y = self.menu_y
        icon_x = self.menu_x
        
        if self.new_folder_copy == 0:
            files = "New Folder"
        else:
            files = f"New Folder ({self.new_folder_copy})"
        if os.path.exists(f"{variables.users}\\{Auth.username}\\desktop\\{files}"):
            self.new_folder_copy += 1
            self.new_folder()
            return

        os.makedirs(f"{variables.users}\\{Auth.username}\\desktop\\{files}")

        self.image = self.desktop.create_image(icon_x, icon_y, image=self.folders, tags=files.replace(' ', '/'))
        self.img_ref.append(self.icon_photo)
        self.img_ref.append(self.folders)
        text = self.desktop.create_text(icon_x,
                                        icon_y + 30,
                                        text=files[:15] + "..." if len(files) > 15 else files,
                                        anchor="n", font=("Arial", 11))
        self.text_ref.append(text)
        image_id = len(self.icon_dict)+1
        self.icon_dict[files.replace(' ', '/')] = (icon_x, icon_y)
        
        x = int(icon_x/100)*100
        y = int(icon_y/100)*100
        if self.grid == False:
            return
        self.desktop.coords(self.image, x+50, y+50)
        self.desktop.coords(text, x+50, y+80 )

        self.desktop.tag_bind(self.image, "<Button-1>", lambda event, img=self.image, txt=text: self.on_image_press(event, img, txt))
        self.desktop.tag_bind(self.image, "<Button-3>", self.icon_popup)
        #self.desktop.tag_bind(text, "<Double-1>", lambda event, txt=text, file=files: self.on_img_rename(event, txt, file))
        self.desktop.tag_bind(self.image, "<B1-Motion>", lambda event, img=self.image, txt=text: self.on_image_move(event, img, txt))
        self.desktop.tag_bind(self.image, "<ButtonRelease-1>", lambda event, img=self.image, txt=text: self.on_image_release(event, img, txt))

    #sub menus
    def do_popup(self, event):
        self.menu_x = event.x_root
        self.menu_y = event.y_root
        try:
            self.desktop_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.desktop_menu.grab_release()

    def icon_popup(self, event):
        self.menu_x = event.x_root
        self.menu_y = event.y_root
        try:
            self.icon_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.icon_menu.grab_release()

    def icon_size(self, max, size, height, add, initialized):
        self.icon_max = max
        self.icon_numsize = size
        self.height = height
        self.add = add
        if height == 80:
            self.icon_photo = PhotoImage(file=os.path.join(variables.icon_images, "UnknownIcon_Large.png"))
            self.folders = PhotoImage(file=os.path.join(variables.icon_images, "Folder_large.png"))

            if initialized:
                return
            
            if self.icon_size_var_set == 'large':
                pass
            if self.icon_size_var_set == 'medium':
                for i in self.icon_dict:
                    icon_x, icon_y = self.icon_dict[i]
                    icon_x = round(icon_x * 1.4)
                    icon_y = round(icon_y * 1.4)
                    self.icon_dict[i] = (icon_x, icon_y)
            if self.icon_size_var_set == 'small':
                for i in self.icon_dict:
                    icon_x, icon_y = self.icon_dict[i]
                    icon_x = round(icon_x * 2.8)
                    icon_y = round(icon_y * 2.8)
                    self.icon_dict[i] = (icon_x, icon_y)
                
        if height == 50:
            self.icon_photo = PhotoImage(file=os.path.join(variables.icon_images, "UnknownIcon_Medium.png"))
            self.folders = PhotoImage(file=os.path.join(variables.icon_images, "Folder_medium.png"))
            if initialized:
                return
            if self.icon_size_var_set == 'large':
                for i in self.icon_dict:
                    icon_x, icon_y = self.icon_dict[i]
                    icon_x = round(icon_x / 1.4)
                    icon_y = round(icon_y / 1.4)
                    self.icon_dict[i] = (icon_x, icon_y)
            if self.icon_size_var_set == 'medium':
                pass
            if self.icon_size_var_set == 'small':
                for i in self.icon_dict:
                    icon_x, icon_y = self.icon_dict[i]
                    icon_x = round(icon_x * 1.4)
                    icon_y = round(icon_y * 1.4)
                    self.icon_dict[i] = (icon_x, icon_y)
        if height == 35:
            self.icon_photo = PhotoImage(file=os.path.join(variables.icon_images, "UnknownIcon_Medium.png"))
            self.folders = ImageTk.PhotoImage(Image.open(os.path.join(variables.icon_images, "Folder_medium.png")))
            if initialized:
                return
            if self.icon_size_var_set == 'large':
                for i in self.icon_dict:
                    icon_x, icon_y = self.icon_dict[i]
                    icon_x = round(icon_x / 2.8)
                    icon_y = round(icon_y / 2.8)
                    self.icon_dict[i] = (icon_x, icon_y)
            if self.icon_size_var_set == 'medium':
                for i in self.icon_dict:
                    icon_x, icon_y = self.icon_dict[i]
                    icon_x = round(icon_x / 1.4)
                    icon_y = round(icon_y / 1.4)
                    self.icon_dict[i] = (icon_x, icon_y)
            if self.icon_size_var_set == 'small':
                pass

        if not self.icon_dict == {}:
            with open(f"{variables.users}\\{Auth.username}\\icon_position.json", "w") as file:
                json.dump(self.icon_dict, file)

        self.icon_height = height
        if not initialized:
            self.place_icons()
        return

    def veiw_icons(self):
        if self.view_icons_value != True:
            self.view_icons_value=True
            self.place_icons()
        else:
            self.view_icons_value=False
            for button in self.desktop.winfo_children():
                if isinstance(button, tk.Button):
                    button.destroy()

    def place_icons(self):
        variables.refresh_var()
        max = self.icon_max
        size = self.icon_numsize
        height = self.height
        add = self.add
        try:
            with open(f"{variables.users}\\{Auth.username}\\icon_position.json", "r") as file:
                self.icon_dict = json.load(file)
        except:
            self.icon_dict = self.icon_dict
        self.icon_size(max, size, height, add, True)
        
        for image in self.img_ref:
            self.desktop.delete(image)

        for text in self.text_ref:
            self.desktop.delete(text)

        icon_y = self.icon_height-add
        icon_x = self.icon_height-add
        self.img_ref = []
        self.text_ref = []

        for files in os.listdir(variables.desktop_list):
            file_path = os.path.join(variables.desktop_list, files)

            if files.replace(' ', '/') in self.icon_dict:
                # If the image already has a location in the dictionary, use that location
                icon_x, icon_y = self.icon_dict[files.replace(' ', '/')]
            else:
                # If the image doesn't have a location in the dictionary, find the next available grid cell
                while self.icon_dict.get("cell_" + str(icon_x) + "_" + str(icon_y)):
                    icon_y += self.icon_numsize
                    if icon_y > self.icon_max:
                        icon_y = -50-(self.add*2)
                        icon_x += self.icon_numsize
                self.icon_dict[files.replace(' ', '/')] = (icon_x, icon_y)
            
            if os.path.isdir(file_path):
                self.image = self.desktop.create_image(icon_x, icon_y, image=self.folders, tags=files.replace(' ', '/'))
            else:
                self.image = self.desktop.create_image(icon_x, icon_y, image=self.icon_photo, tags=files.replace(' ', '/'))

            self.icon_id += 1

            self.img_ref.append(self.icon_photo)
            self.img_ref.append(self.folders)

            text = self.desktop.create_text(icon_x,
                                        icon_y + 30 + (self.add*2+self.add//2),
                                        text=files[:15] + "..." if len(files) > 15 else files,
                                        anchor="n", font=("Arial", 11))
            self.text_ref.append(text)
            
            self.desktop.tag_bind(self.image, "<Button-1>", lambda event, img=self.image, txt=text: self.on_image_press(event, img, txt))
            self.desktop.tag_bind(self.image, "<Button-3>", self.icon_popup)
            self.desktop.tag_bind(text, "<Double-1>", lambda event, txt=text, file=files: self.on_img_rename(event, txt, file))
            self.desktop.tag_bind(self.image, "<B1-Motion>", lambda event, img=self.image, txt=text: self.on_image_move(event, img, txt))
            self.desktop.tag_bind(self.image, "<ButtonRelease-1>", lambda event, img=self.image, txt=text: self.on_image_release(event, img, txt))


            if icon_y > self.icon_max:
                icon_y = -50-(self.add*2)
                icon_x += self.icon_numsize
            icon_y += self.icon_numsize

        self.icon_id = 0

    def on_image_press(self, event, img, txt):
        self.selected_img = img
        self.desktop.configure(cursor="fleur")
        self.desktop.x = event.x
        self.desktop.y = event.y
        self.desktop.coords(img, self.x, self.y)
        self.desktop.coords(txt, self.x, self.y)

    def on_img_rename(self, event, text, file_name):
        self.rename_text_box = tk.Entry(window)
        self.rename_text_box.bind('<Return>', lambda event, txt=text, file=file_name: self.update_icon_name(event, txt, file))
        self.desktop.create_window(event.x, event.y, window=self.rename_text_box, tag='entry')

    def update_icon_name(self, event, text, file_name):
        self.desktop.delete('entry')
        self.desktop.itemconfig(text, text=self.rename_text_box.get())
        self.desktop.itemconfig(file_name, tag=self.rename_text_box.get().replace(' ', '/'))
        os.rename(f"{variables.desktop_list}\\{file_name}", f"{variables.desktop_list}\\{self.rename_text_box.get()}")
        icon_x, icon_y = self.icon_dict[file_name.replace(' ', '/')]
        del self.icon_dict[file_name.replace(' ', '/')]
        self.icon_dict[self.rename_text_box.get().replace(' ', '/')] = icon_x, icon_y
        
    # function to handle the move event
    def on_image_move(self, event, img, txt):
        image_id = self.desktop.gettags(img)[0]
        location = self.icon_dict[image_id]

        if self.selected_img == img:
            x, y = (event.x - self.desktop.x), (event.y - self.desktop.y)
            self.desktop.move(self.selected_img, x, y)
            self.desktop.move(txt, x, y)
            self.desktop.x = event.x
            self.desktop.y = event.y

    # function to handle the release event
    def on_image_release(self, event, img, txt):
        self.desktop.configure(cursor="")
        x = int(event.x/self.icon_numsize)*self.icon_numsize
        y = int(event.y/self.icon_numsize)*self.icon_numsize
        if self.grid == False:
            return
        self.desktop.coords(img, x+self.icon_numsize//2, y+self.icon_numsize//2)
        self.desktop.coords(txt, x+self.icon_numsize//2, y+self.height+self.height//2+5 )

        # update location of the image in the dictionary
        image_id = self.desktop.gettags(img)[0]
        self.icon_dict[image_id] = (x+self.icon_numsize//2, y+self.icon_numsize//2)
        with open(f"{variables.users}\\{Auth.username}\\icon_position.json", "w") as file:
            json.dump(self.icon_dict, file)

    def align_grid(self):
        if self.grid == True:
            self.grid=False
        else:
            self.grid=True
            for button in self.desktop.winfo_children():
                if isinstance(button, tk.Canvas):
                    x = ((button.winfo_x()/100)*100)
                    y = ((button.winfo_y() + self.icon_numsize//2) // self.icon_numsize) * self.icon_numsize

                    # check if there is already a button at this position
                    for existing_button in self.desktop.winfo_children():
                        if isinstance(existing_button, tk.Button) and existing_button != button:
                            if existing_button.winfo_x() == x and existing_button.winfo_y() == y:
                                self.file_icon.place(x=existing_button.winfo_x()+self.icon_numsize, y=existing_button.winfo_y()+self.icon_numsize)
                                return
                    button.place_configure(x=x,y=y)

if __name__ == "__main__":
    variables = Variables()
    if not os.path.exists(f"{variables.current_directory}\\Users"):
        os.mkdir(f"{variables.current_directory}\\Users")
    #os.system('taskkill /f /im explorer.exe')
    #atexit.register(exit_handler)
    window = App()
    signup_screen = Signup_screen(window)
    window.mainloop()
