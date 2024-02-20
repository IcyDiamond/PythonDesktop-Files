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


update_version = "1.1.7"
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
        self.signin_screen = Signin_screen(self)

class Variables:
    def __init__(self):
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.desktop_files = os.path.dirname(os.path.abspath(__file__))
        self.users = os.path.join(self.desktop_files, "users")
        self.file_explorer = os.path.join(self.desktop_files, "FileExplorer.py")
        self.desktop_list = f"{self.users}\\{Auth.username}\\desktop"
        self.assets = os.path.join(f"{self.desktop_files}\\Windows\\system32")

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
        self.assets = os.path.join(f"{self.desktop_files}\\Windows\\system32")
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
class Signin_screen:
    def __init__(self, master):
        self.master = master
        self.initialized = False
        self.initialize_object()

    #Set up the window with the widgets
    def initialize_object(self):
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
        self.desktop.initialize_object()
    
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
        self.signup_screen.initialize_object()
        
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

class Signup_screen:
    def __init__(self, master):
        self.master = master        

    def initialize_object(self):
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
        self.master.signin_screen = Signin_screen(self.master)

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

        self.master.signin_screen = Signin_screen(self.master)
        self.master.signin_screen.initialize_object()

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

class Desktop_screen:
    def __init__(self, master):
        self.master = master
        self.icons = []
        self.icon_ref = []
        self.icon_dict = {}
        self.icon_base_text_size = {}
        self.view_icons_value = True
        self.grid=True
        self.new_folder_copy = 0
        self.menu_x = 0
        self.menu_y = 0
        self.show_start_menu = True
        self.side_bar_initialized = False
        self.side_bar_active = False
        self.icon_left = False
        self.start_menu = None
        self.image = None
        self.x = None
        self.y = None
        self.current_icon_hover = None
        self.icon_id = 0
        self.monitor_height = variables.monitor_height
        self.monitor_width = variables.monitor_width
        
        self.icon_numsize = 100
        self.height = 54
        self.add = 0

        #numbers for default rounding to grid
        self.pady = 1.19
        self.y_offset = 38
        self.padx = 76
        self.x_offset = 38

    def initialize_taskbar(self):
        self.new_window = tk.Toplevel(self.master)
        Taskbar(self.new_window, self)

    def refresh_taskbar(self):
        self.new_window.destroy()
        self.initialize_taskbar()

    def initialize_object(self):
        #clears any widgets
        for widgets in self.master.signin_frame.winfo_children():
            widgets.destroy()
        window.attributes('-fullscreen',True)
        self.master.signin_frame.pack_forget()
        self.master.signup_frame.pack_forget()
        self.master.desktop_frame.pack(fill=BOTH, expand=True)
        self.initialize_taskbar()

        #wallpaper
        self.icon_photo = PhotoImage(file=os.path.join(variables.assets, "UnknownIcon_Medium.png"))
        self.wallpaper = ImageTk.PhotoImage(Image.open(os.path.join(f"{variables.current_directory}\\Windows\\Web\\Wallpaper\\Wallpaper.jpg")).resize((self.monitor_width, self.monitor_height)))
        self.folders_small = ImageTk.PhotoImage(Image.open(os.path.join(variables.assets, "Folder_Small.png")))
        self.folders_medium = ImageTk.PhotoImage(Image.open(os.path.join(variables.assets, "Folder_Medium.png")))
        self.folders_large = ImageTk.PhotoImage(Image.open(os.path.join(variables.assets, "Folder_Large.png")))

        self.none_selection_small = ImageTk.PhotoImage(Image.open(os.path.join(variables.assets, "Empty_Icon_Selection.png")).resize((76,54)))
        self.none_selection_medium = ImageTk.PhotoImage(Image.open(os.path.join(variables.assets, "Empty_Icon_Selection.png")).resize((76,70)))
        self.none_selection_large = ImageTk.PhotoImage(Image.open(os.path.join(variables.assets, "Empty_Icon_Selection.png")).resize((106,118)))

        self.hover_selection_small = ImageTk.PhotoImage(Image.open(os.path.join(variables.assets, "Hover_Icon_Selection.png")).resize((76,54)))
        self.hover_selection_small_wtext = ImageTk.PhotoImage(Image.open(os.path.join(variables.assets, "Hover_Icon_Selection.png")).resize((76,69)))
        self.hover_selection_medium = ImageTk.PhotoImage(Image.open(os.path.join(variables.assets, "Hover_Icon_Selection.png")).resize((76,70)))
        self.hover_selection_medium_wtext = ImageTk.PhotoImage(Image.open(os.path.join(variables.assets, "Hover_Icon_Selection.png")).resize((76,85)))
        self.hover_selection_large = ImageTk.PhotoImage(Image.open(os.path.join(variables.assets, "Hover_Icon_Selection.png")).resize((106,118)))

        self.clicked_selection_small = ImageTk.PhotoImage(Image.open(os.path.join(variables.assets, "Clicked_Icon_Selection.png")).resize((76,54)))
        self.clicked_selection_small_wtext = ImageTk.PhotoImage(Image.open(os.path.join(variables.assets, "Clicked_Icon_Selection.png")).resize((76,69)))
        self.clicked_selection_medium = ImageTk.PhotoImage(Image.open(os.path.join(variables.assets, "Clicked_Icon_Selection.png")).resize((76,70)))
        self.clicked_selection_medium_wtext = ImageTk.PhotoImage(Image.open(os.path.join(variables.assets, "Clicked_Icon_Selection.png")).resize((76,85)))
        self.clicked_selection_large = ImageTk.PhotoImage(Image.open(os.path.join(variables.assets, "Clicked_Icon_Selection.png")).resize((106,118)))

        self.hover_clicked_selection_small = ImageTk.PhotoImage(Image.open(os.path.join(variables.assets, "Hover_Clicked_Icon_Selection.png")).resize((76,54)))
        self.hover_clicked_selection_small_wtext = ImageTk.PhotoImage(Image.open(os.path.join(variables.assets, "Hover_Clicked_Icon_Selection.png")).resize((76,69)))
        self.hover_clicked_selection_medium = ImageTk.PhotoImage(Image.open(os.path.join(variables.assets, "Hover_Clicked_Icon_Selection.png")).resize((76,70)))
        self.hover_clicked_selection_medium_wtext = ImageTk.PhotoImage(Image.open(os.path.join(variables.assets, "Hover_Clicked_Icon_Selection.png")).resize((76,85)))
        self.hover_clicked_selection_large = ImageTk.PhotoImage(Image.open(os.path.join(variables.assets, "Hover_Clicked_Icon_Selection.png")).resize((106,118)))



        #default
        self.clicked_selection = self.clicked_selection_small
        self.hover_selection = self.hover_selection_small
        self.none_selection = self.none_selection_small
        self.folders = self.folders_small
        self.hover_selection_wtext = self.hover_selection_small_wtext
        self.clicked_selection_wtext = self.clicked_selection_small_wtext
        self.hover_clicked_selection = self.hover_clicked_selection_small
        self.hover_clicked_selection_wtext = self.hover_clicked_selection_small_wtext
        self.y_text_offset = 7

        self.desktop = tk.Canvas(self.master.desktop_frame, bg="black", highlightthickness=0)
        self.desktop.pack(side=LEFT,fill=BOTH, expand=True)
        self.desktop.create_image(0, 0, image = self.wallpaper, anchor = NW)


        #icons
        self.icon_size_var_set = 'small'
        self.selected_base = None
        self.selected_text = None
        self.icon_movement = False
        self.icon_focused = False

        self.start_x = 0
        self.start_y = 0
        self.max_text_width = 68
        self.rect = None

        self.desktop.bind('<ButtonPress-1>', self.on_press)
        self.desktop.bind('<B1-Motion>', self.on_drag)
        self.desktop.bind('<ButtonRelease-1>', self.on_release)
        self.desktop.bind("<Double-1>", lambda x: print("test"))
        
        self.place_icons()
        
        #----------------------------------------Work in progress (context menu)--------------------------------------------------------------------

        #makes the right click menu on desktop
        self.desktop_menu = tk.Menu(self.master.desktop_frame, tearoff=0)
        self.icon_menu = tk.Menu(self.master.desktop_frame, tearoff=0)
        self.desktop_submenu = tk.Menu(self.master.desktop_frame, tearoff=0)

        #view sub menu
        self.view_icons_var = tk.BooleanVar()
        self.align_grid_var = tk.BooleanVar()
        self.icon_size_var = tk.StringVar()
        self.icon_size_var.set("small")
        self.align_grid_var.set(True)
        self.view_icons_var.set(True)
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
        self.desktop_submenu.entryconfig("Small icons", state="normal")

        self.desktop_submenu.entryconfig("Auto Arrange icons", state="disabled")
        self.desktop_submenu.entryconfig("Align icons to grid", state="normal")

        self.desktop_submenu.entryconfig("Show desktop icons",  state="normal")

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

    def on_press(self, event):
        self.start_x = event.x_root
        self.start_y = event.y_root
        for base, __ in self.icon_dict.items():
            self.desktop.itemconfig(base+"base", image=self.none_selection)
        if self.icon_focused == False:
            self.desktop.itemconfig(self.selected_base, image=self.none_selection)
        else:
            for i in self.desktop.gettags(self.selected_text):
                try:
                    if int(i) <= 16:
                        self.desktop.itemconfig(self.selected_base, image=self.clicked_selection)
                    else:
                        self.desktop.itemconfig(self.selected_base, image=self.clicked_selection_wtext)
                except ValueError:
            #        #because it gives tag Current which cant be a int
                    pass
        self.rect = self.desktop.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='blue', fill='blue', stipple='gray25'
        )
        

    def on_drag(self, event):
        if self.rect:
            current_x = event.x_root
            current_y = event.y_root
            if not self.icon_movement:
                for base, values_list in self.icon_dict.items():
                    for i in values_list:
                        icon_x = values_list[0]
                        icon_y = values_list[1]
                        if ((icon_x < self.start_x and icon_x > event.x_root) or (icon_x > self.start_x and icon_x < event.x_root)) and ((icon_y < self.start_y and icon_y > event.y_root) or (icon_y > self.start_y and icon_y < event.y_root)):
                            text, height, icon_x, icon_y = self.icon_base_text_size[base+"base"]
                            if not height <= 16:
                                self.desktop.itemconfig(base+"base", image=self.clicked_selection_wtext)
                            else:
                                self.desktop.itemconfig(base+"base", image=self.clicked_selection)
                            break
                        else:
                            self.desktop.itemconfig(base+"base", image=self.none_selection)
                            break

                self.desktop.coords(self.rect, self.start_x, self.start_y, current_x, current_y)
            else:
                self.desktop.delete(self.rect)

    def on_release(self, event):
        if self.rect:
            self.desktop.delete(self.rect)

    def set_icon_size(self):
        # Get the selected icon size
        icon_size = self.icon_size_var.get()

        if icon_size == "large":
            self.icon_size("large", 118, 10)
            self.icon_size_var_set = 'large'
        elif icon_size == "medium":
            self.icon_size("medium", 70, 0)
            self.icon_size_var_set = 'medium'
        elif icon_size == "small":
            self.icon_size("small", 54, -10)
            self.icon_size_var_set = 'small'

    def new_folder(self):
        icon_y = self.menu_y
        icon_x = self.menu_x
        
        if self.new_folder_copy == 0:
            files = "New Folder"
        else:
            files = f"New Folder ({self.new_folder_copy+1})"
        if os.path.exists(f"{variables.users}\\{Auth.username}\\desktop\\{files}"):
            self.new_folder_copy += 1
            self.new_folder()
            return
        
        os.makedirs(f"{variables.users}\\{Auth.username}\\desktop\\{files}")

        file_path = f"{variables.users}\\{Auth.username}\\desktop\\{files}"

        self.create_icons(file_path, files, icon_x, icon_y)

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

    def icon_size(self, size, height, add):
        self.height = height
        self.add = add
        if size == "large":
            self.icon_photo = PhotoImage(file=os.path.join(variables.assets, "UnknownIcon_Large.png"))
            self.folders = self.folders_large
            self.none_selection = self.none_selection_large
            self.hover_selection = self.hover_selection_large
            self.clicked_selection = self.clicked_selection_large

            self.pady = .82 #all broken
            self.y_offset = 65 #all broken
            self.padx = 106 #all broken
            self.x_offset = 56 

            self.y_text_offset = 32
            self.max_text_width = 98

            
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
                    icon_x = round(icon_x * 1.4)
                    icon_y = round(icon_y * 1.4)
                    self.icon_dict[i] = (icon_x, icon_y)
                
        if size == "medium":
            self.icon_photo = PhotoImage(file=os.path.join(variables.assets, "UnknownIcon_Medium.png"))
            self.folders = self.folders_medium
            self.none_selection = self.none_selection_medium
            self.hover_selection = self.hover_selection_medium
            self.clicked_selection = self.clicked_selection_medium
            self.hover_selection_wtext = self.hover_selection_medium_wtext
            self.clicked_selection_wtext = self.clicked_selection_medium_wtext

            self.pady = .99 #Still not perfect
            self.y_offset = 76
            self.padx = 76
            self.x_offset = 38

            self.y_text_offset = 14
            self.max_text_width = 68

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
                    #icon_x = round(icon_x * 1.4)
                    icon_y = round(icon_y * 1.2)
                    self.icon_dict[i] = (icon_x, icon_y)
        if size == "small":
            self.icon_photo = NONE
            self.folders = self.folders_small
            self.none_selection = self.none_selection_small
            self.hover_selection = self.hover_selection_small
            self.clicked_selection = self.clicked_selection_small
            self.hover_selection_wtext = self.hover_selection_small_wtext
            self.clicked_selection_wtext = self.clicked_selection_small_wtext

            self.pady = 1.19
            self.y_offset = 38
            self.padx = 76
            self.x_offset = 38

            self.y_text_offset = 7
            self.max_text_width = 68

            if self.icon_size_var_set == 'large':
                for i in self.icon_dict:
                    icon_x, icon_y = self.icon_dict[i]
                    icon_x = round(icon_x / 1.4)
                    icon_y = round(icon_y / 1.4)
                    self.icon_dict[i] = (icon_x, icon_y)
            if self.icon_size_var_set == 'medium':
                for i in self.icon_dict:
                    icon_x, icon_y = self.icon_dict[i]
                    #icon_x = round(icon_x / 1.4)
                    icon_y = round(icon_y / 1.2)
                    self.icon_dict[i] = (icon_x, icon_y)
            if self.icon_size_var_set == 'small':
                pass

        if not self.icon_dict == {}:
            self.file_dump()

        self.place_icons()

    def veiw_icons(self):
        if self.view_icons_value != True:
            self.view_icons_value=True
            for icon in self.icon_ref:
                try:
                    self.desktop.itemconfig(icon, state=tk.NORMAL)
                except tk.TclError:
                    self.icon_ref.remove(icon)
        else:
            self.view_icons_value=False
            for icon in self.icon_ref:
                try:
                    self.desktop.itemconfig(icon, state=tk.HIDDEN)
                except tk.TclError:
                    self.icon_ref.remove(icon)

    def shorten_text(self, files, icon_x, icon_y):
        lines = []
        current_line = ""
        
        for word in files.split():
            text_line = current_line + " " + word if current_line else word
            text = self.desktop.create_text(icon_x-32, icon_y, text=text_line, font=("Arial", 10), anchor="n")
            bounds = self.desktop.bbox(text)
            text_width = bounds[2] - bounds[0]
            text_height = bounds[3] - bounds[1]
            self.desktop.delete(text)
            
            if text_width <= self.max_text_width:
                current_line = text_line
            else: 
                if current_line:
                    lines.append((current_line, text_height))
                current_line = word
        
        if current_line:
            lines.append((current_line, text_height))

        # Calculate max_line_width as you have it
        max_line_width = max([self.desktop.bbox(self.desktop.create_text(0, 0, text=line, font=("Arial", 10), anchor="n", tags="Placeholder"))[2] - 
                            self.desktop.bbox(self.desktop.create_text(0, 0, text=line, font=("Arial", 10), anchor="n", tags="Placeholder"))[0] 
                            for line, _ in lines])

        # Hide the text items
        for text_item in self.desktop.find_withtag("Placeholder"):
            self.desktop.itemconfigure(text_item, state=tk.HIDDEN)

        
        # Add "..." to lines that exceed max_width
        truncated_lines = []
        total_height = 0
        for line, height in lines:
            text = self.desktop.create_text(icon_x-32, icon_y, text=line, font=("Arial", 10), anchor="n")
            bounds = self.desktop.bbox(text)
            text_width = bounds[2] - bounds[0]
            self.desktop.delete(text)
            
            if text_width <= self.max_text_width:
                padding = " " * ((max_line_width - text_width) // 8)  # Calculate padding to center the line
                truncated_lines.append(padding + line)
            else:
                truncated_lines.append(line[:-3] + "...")

            total_height += height
        
        # Create the text item on the Canvas
        truncated_text = "\n".join(truncated_lines)
        text = self.desktop.create_text(icon_x-32, icon_y, text=truncated_text, font=("Arial", 10), anchor="nw", fill='#ffffff', tags=total_height)
        
        return text, total_height

    def place_icons(self):
        variables.refresh_var()
        icon_y = self.height-self.add #used to find spot if no location
        icon_x = self.height-self.add #used to find spot if no location

        try:
            with open(f"{variables.users}\\{Auth.username}\\icon_position.json", "r") as file:
                self.icon_dict = json.load(file)
        except:
            self.icon_dict = self.icon_dict
        
        for icon in self.icon_ref:
            self.desktop.delete(icon)
#
        self.icon_ref = []
#
        for files in os.listdir(variables.desktop_list):
            file_path = os.path.join(variables.desktop_list, files)

            if files.replace(' ', '/') in self.icon_dict:
                # If the image already has a location in the dictionary, use that location
                icon_x, icon_y = self.icon_dict[files.replace(' ', '/')]
            #else:
                # If the image doesn't have a location in the dictionary, find the next available grid cell
                #while self.icon_dict.get("cell_" + str(icon_x) + "_" + str(icon_y)):
                #    icon_y += self.icon_numsize
                #    if icon_y > self.icon_max:
                #        icon_y = -50-(self.add*2)
                #        icon_x += self.icon_numsize
                #self.icon_dict[files.replace(' ', '/')] = (icon_x, icon_y)
            
            self.create_icons(file_path, files, icon_x, icon_y)

            #find the next available spot 
            if icon_y > self.monitor_height-40-70: #Taskbar height #used to find spot if no location 
                icon_y = -50-(self.add*2) #useless currently (self.add) #used to find spot if no location
                icon_x += self.icon_numsize #used to find spot if no location
            icon_y += self.icon_numsize #used to find spot if no location

        self.icon_id = 0

    def create_icons(self, file_path, files, icon_x, icon_y):
        if self.view_icons_value == False:
            view = tk.HIDDEN
        else:
            view = tk.NORMAL

        text, height = self.shorten_text(files, icon_x, icon_y+self.y_text_offset)
        
        if os.path.isdir(file_path):
            if not height <= 16:
                self.desktop_icon_base = self.desktop.create_image(icon_x, icon_y+7, image=self.none_selection, tags=files.replace(' ', '/')+"base")
            else:
                self.desktop_icon_base = self.desktop.create_image(icon_x, icon_y, image=self.none_selection, tags=files.replace(' ', '/')+"base")
            self.image = self.desktop.create_image(icon_x, icon_y-8, image=self.folders, tags=files.replace(' ', '/'))
    #    else:
    #        self.image = self.desktop.create_image(icon_x, icon_y, image=self.icon_photo, tags=files.replace(' ', '/'))

        self.icon_base_text_size[files.replace(' ', '/')+"base"] = text, height, icon_x, icon_y+self.y_text_offset

        self.icon_id += 1           
        
        self.desktop.itemconfig(self.desktop_icon_base, state=view)
        self.desktop.itemconfig(self.image, state=view)
        self.desktop.itemconfig(text, state=view)
#
        self.icon_ref.append(self.desktop_icon_base)
        self.icon_ref.append(self.icon_photo)
        self.icon_ref.append(self.folders)
        self.icon_ref.append(self.image)
        self.icon_ref.append(text)
    #    
        self.desktop.tag_bind(self.desktop_icon_base, "<ButtonRelease-1>", lambda event, base=self.desktop_icon_base, img=self.image, txt=text: self.on_image_release(event, base, img, txt))
        self.desktop.tag_bind(self.desktop_icon_base, "<B1-Motion>", lambda event, base=self.desktop_icon_base, img=self.image, txt=text: self.on_image_move(event, base, img, txt))
        self.desktop.tag_bind(self.desktop_icon_base, "<Button-1>", lambda event, base=self.desktop_icon_base, img=self.image, txt=text: self.on_image_press(event, base, img, txt))
        self.desktop.tag_bind(self.desktop_icon_base, "<Enter>", lambda event, base=self.desktop_icon_base, img=self.image, txt=text: self.on_icon_hover(event, base, img, txt))
        self.desktop.tag_bind(self.desktop_icon_base, "<Leave>", lambda event, base=self.desktop_icon_base, img=self.image, txt=text: self.on_icon_leave(event, base, img, txt))
        self.desktop.tag_bind(self.desktop_icon_base, "<Key>", lambda event, base=self.desktop_icon_base, img=self.image, txt=text: self.on_icon_delete(event, base, img, txt))
        self.desktop.tag_bind(self.image, "<ButtonRelease-1>", lambda event, base=self.desktop_icon_base, img=self.image, txt=text: self.on_image_release(event, base, img, txt))
        self.desktop.tag_bind(self.image, "<B1-Motion>", lambda event, base=self.desktop_icon_base, img=self.image, txt=text: self.on_image_move(event, base, img, txt))
        self.desktop.tag_bind(self.image, "<Button-1>", lambda event, base=self.desktop_icon_base, img=self.image, txt=text: self.on_image_press(event, base, img, txt))
        self.desktop.tag_bind(self.image, "<Enter>", lambda event, base=self.desktop_icon_base, img=self.image, txt=text: self.on_icon_hover(event, base, img, txt))
        self.desktop.tag_bind(self.image, "<Leave>", lambda event, base=self.desktop_icon_base, img=self.image, txt=text: self.on_icon_leave(event, base, img, txt))
        #self.desktop.tag_bind(self.image, "<BackSpace>", lambda event, base=self.desktop_icon_base, img=self.image, txt=text: self.on_icon_delete(event, base, img, txt))
        #self.desktop.tag_bind(self.image, "<Button-3>", self.icon_popup)
        self.desktop.tag_bind(text, "<ButtonRelease-1>", lambda event, base=self.desktop_icon_base, img=self.image, txt=text: self.on_image_release(event, base, img, txt))
        self.desktop.tag_bind(text, "<B1-Motion>", lambda event, base=self.desktop_icon_base, img=self.image, txt=text: self.on_image_move(event, base, img, txt))
        self.desktop.tag_bind(text, "<Button-1>", lambda event, base=self.desktop_icon_base, img=self.image, txt=text: self.on_image_press(event, base, img, txt))
        self.desktop.tag_bind(text, "<Double-1>", lambda event, txt=text, file=files: self.on_img_rename(event, txt, file))
        self.desktop.tag_bind(text, "<Enter>", lambda event, base=self.desktop_icon_base, img=self.image, txt=text: self.on_icon_hover(event, base, img, txt))
        self.desktop.tag_bind(text, "<Leave>", lambda event, base=self.desktop_icon_base, img=self.image, txt=text: self.on_icon_leave(event, base, img, txt))
        #self.desktop.tag_bind(text, "<BackSpace>", lambda event, base=self.desktop_icon_base, img=self.image, txt=text: self.on_icon_delete(event, base, img, txt))

    def on_icon_hover(self, event, base, img, txt):
        if self.selected_base == base:
            pass
        else:
            if not self.icon_left:
                for i in self.desktop.gettags(txt):
                    try:
                        if int(i) <= 16:
                            current_image = self.desktop.itemcget(base, 'image')
                            if str(current_image) == str(self.clicked_selection):
                                self.desktop.itemconfig(base, image=self.hover_clicked_selection)
                            else:
                                self.desktop.itemconfig(base, image=self.hover_selection)
                        else:
                            current_image = self.desktop.itemcget(base, 'image')
                            if str(current_image) == str(self.clicked_selection_wtext):
                                self.desktop.itemconfig(base, image=self.hover_clicked_selection_wtext)
                            else:
                                self.desktop.itemconfig(base, image=self.hover_selection_wtext)

                    except ValueError:
                        #because it gives tag Current which cant be a int
                        pass
        self.current_icon_hover = base

    def on_icon_leave(self, event, base, img, txt):
        self.icon_left = True
        if self.selected_base == base:
            pass
        else:
            current_image = self.desktop.itemcget(base, 'image')
            if str(current_image) == str(self.hover_clicked_selection):
                self.desktop.itemconfig(base, image=self.clicked_selection)
            elif str(current_image) == str(self.hover_clicked_selection_wtext):
                self.desktop.itemconfig(base, image=self.clicked_selection_wtext)
            else:
                self.desktop.itemconfig(base, image=self.none_selection)
        self.icon_left = False

    def on_image_press(self, event, base, img, txt):
        self.icon_focused = True
        if not self.selected_base == base:
            self.desktop.itemconfig(self.selected_base, image=self.none_selection)
        self.selected_base = base
        self.selected_text = txt
        #self.desktop.itemconfig(base, image=self.clicked_selection)
        self.desktop.configure(cursor="fleur")
        self.desktop.x = event.x
        self.desktop.y = event.y
        self.desktop.coords(img, self.x, self.y)
        self.desktop.coords(txt, self.x, self.y)

    def on_img_rename(self, event, text, file_name):
        self.rename_text_box = tk.Entry(window)
        self.rename_text_box.bind('<Return>', lambda event, txt=text, file=file_name: self.update_icon_name(event, txt, file))
        self.desktop.create_window(event.x, event.y, window=self.rename_text_box, tag='entry')

    def on_icon_delete(self, event, base, img, txt):
        print("removed")
        #os.remove(f"{variables.users}\\{Auth.username}\\desktop\\{base}")

    def update_icon_name(self, event, text, file_name):
        self.desktop.delete('entry')
        self.desktop.itemconfig(text, text=self.rename_text_box.get())
        self.desktop.itemconfig(file_name, tag=self.rename_text_box.get().replace(' ', '/'))
        os.rename(f"{variables.desktop_list}\\{file_name}", f"{variables.desktop_list}\\{self.rename_text_box.get()}")
        icon_x, icon_y = self.icon_dict[file_name.replace(' ', '/')]
        del self.icon_dict[file_name.replace(' ', '/')]
        self.icon_dict[self.rename_text_box.get().replace(' ', '/')] = icon_x, icon_y
        
    # function to handle the move event
    def on_image_move(self, event, base, img, txt):
        if self.selected_base == base:
            self.icon_movement = True
            x, y = (event.x - self.desktop.x), (event.y - self.desktop.y)
            x_coords, y_coords = self.desktop.coords(self.selected_base)
            if event.x > self.monitor_width:
                self.desktop.move(self.selected_base, 0, y)
                self.desktop.move(img, 0, y)
                self.desktop.move(txt, 0, y)
                self.desktop.x = event.x
                self.desktop.y = event.y
            elif event.x < 0:
                self.desktop.move(self.selected_base, 0, y)
                self.desktop.move(img, 0, y)
                self.desktop.move(txt, 0, y)
                self.desktop.x = event.x
                self.desktop.y = event.y
            else:
                self.desktop.move(self.selected_base, x, y)
                self.desktop.move(img, x, y)
                self.desktop.move(txt, x, y)
                self.desktop.x = event.x
                self.desktop.y = event.y

    # function to handle the release event
    def on_image_release(self, event, base, img, txt):
        os.system("cls")
        self.icon_movement = False
        self.icon_focused = False
        self.desktop.configure(cursor="")
        icon_x, icon_y = self.desktop.coords(base)
        print(icon_y)

        x, y = self.round_grid(icon_x, icon_y)
        print(y)

        if self.grid == False:
            x, y = self.desktop.coords(base)
            x, y = self.desktop.coords(img)
            x, y = round(x), round(y)
        else:
            for i in self.desktop.gettags(txt):
                try:
                    if int(i) <= 16:
                        z =  0
                    else:
                        z = 7
                except ValueError:
                    #because it gives tag Current which cant be a int
                    pass
            self.desktop.coords(base, x, y+z)
            self.desktop.coords(img, x, y-8)
            self.desktop.coords(txt, x-32, y+self.y_text_offset)

        # update location of the image in the dictionary
        image_id = self.desktop.gettags(img)[0]
        self.icon_dict[image_id] = (x, y)
        self.file_dump()

    def file_dump(self):
        with open(f"{variables.users}\\{Auth.username}\\icon_position.json", "w") as file:
            json.dump(self.icon_dict, file)
        return

    def align_grid(self):
        if self.grid == True:
            self.grid=False
        else:
            for i in self.icon_dict:
                icon_x, icon_y = self.icon_dict[i]

                x, y = self.round_grid(icon_x, icon_y)

                self.icon_dict[i] = x, y
            self.grid=True
        self.file_dump()
        self.place_icons()

    def round_grid(self, icon_x, icon_y):
        x = int(((icon_x + self.icon_numsize // 2 - self.x_offset) // self.padx) * self.padx + self.x_offset)
        y = int((int(icon_y / (self.icon_numsize / self.pady)) * (self.icon_numsize / self.pady)) + self.y_offset)
        return x, y

if __name__ == "__main__":
    variables = Variables()
    if not os.path.exists(f"{variables.current_directory}\\Users"):
        os.mkdir(f"{variables.current_directory}\\Users")
    #os.system('taskkill /f /im explorer.exe')
    #atexit.register(exit_handler)
    window = App()
    window.mainloop()