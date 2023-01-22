from tkinter.constants import *
from PIL import Image, ImageTk
from tkinter import messagebox
import tkinter as tk
import subprocess
import math
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("300x400")
        self.title("Python Desktop")
        self.login_frame = tk.Frame(self)
        self.signup_frame = tk.Frame(self)
        self.desktop_frame = tk.Frame(self)
        self.login_frame.grid_propagate(0)
        self.signup_frame.grid_propagate(0)
        self.desktop_frame.grid_propagate(0)
        self.login_screen = Login_screen(self)

class Variables:
    desktop_files = os.path.dirname(os.path.abspath(__file__))
    file_explorer = os.path.join(desktop_files, "FileExplorer.py")
    desktop_list = os.listdir(desktop_files)

class Auth():
    username = ""
    password = ""
    username_stored = ""
    username_input_value = True
    password_input_value = True
    username_stored_value = False
    confirm_password_input_value = True

#login screen
class Login_screen:
    def __init__(self, master):
        self.master = master
        self.initialized = False
        self.initialize_obj()

    def initialize_obj(self):
        if not self.initialized:
            #places the login frame
            self.master.login_frame.pack()

            #clears any widgets
            for widgets in self.master.signup_frame.winfo_children():
                widgets.destroy()
            self.master.signup_frame.pack_forget()

            #makes all the input fields and login button
            self.username_input = tk.Entry(self.master.login_frame,bg="light gray",validate="key")
            self.password_input = tk.Entry(self.master.login_frame,bg="light gray",validate="key")
            self.login_button = tk.Button(self.master.login_frame, width=16, text="Login", command=self.login, bg="Green")
            self.link = tk.Label(self.master.login_frame, text="Need an account? S\u0332I\u0332G\u0332N\u0332 \u0332U\u0332P\u0332",font=('Helveticabold', 8), cursor="hand2")

            #places the widgets onto the screen
            self.username_input.pack()
            self.password_input.pack()
            self.login_button.pack()
            self.link.pack()

            #Fills the input fields
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
            self.stored_check()
            self.initialized = True

    def validate(self, P):
        #only allow A-Z, a-z, 0-9, and common symbols
        return all(c.isalnum() or c in '!@#$%^&*()_-+=[]{}\\|;:\'",.<>?/' for c in P)

    #Check all the info in the inputs
    def login(self):
        if self.username_input.get().isspace() or self.username_input.get() in ["Username",""]:
            messagebox.showerror("Error", "Field above can not be blank!")
        else:
            if self.password_input.get().isspace() or self.password_input.get() in ["Password",""]:
                messagebox.showerror("Error", "Field above can not be blank!")
            else:

                #Change to check info in file
                if self.username_input.get() == Auth.username:
                    if self.password_input.get() == Auth.password:
                        messagebox.showinfo("Success","login successful!")
                        self.username_input_value = True
                        self.password_input_value = True
                        self.desktop = Desktop_screen(self.master)
                        self.desktop.initialize_obj()
                    else:
                        messagebox.showerror("Error", "Username or Password is incorrect!")
                else:
                    messagebox.showerror("Error", "Username or Password is incorrect!")
    
    def stored_check(self):
        if Auth.username_stored_value == True:
            self.username_input.insert(0, Auth.username_stored)
            Auth.username_stored_value = False
        else:
            self.username_input.insert(0, "Username")
        
    def hyperlink(self):
        self.master.login_frame.pack_forget()
        
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
        for widgets in self.master.login_frame.winfo_children():
            widgets.destroy()
        self.master.login_frame.pack_forget()
        
        #makes all the input fields and login button
        self.username_input = tk.Entry(self.master.signup_frame,bg="light gray",validate="key")
        self.password_input = tk.Entry(self.master.signup_frame,bg="light gray",validate="key")
        self.confirm_password_input = tk.Entry(self.master.signup_frame, bg="light gray",validate="key")
        self.signup_button = tk.Button(self.master.signup_frame, width=16, text="SignUp", command=self.signup, bg="Green")
        self.link = tk.Label(self.master.signup_frame, text="Already a User? L\u0332O\u0332G\u0332I\u0332N\u0332",font=('Helveticabold', 8), cursor="hand2")

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
        self.stored_check()

    def validate(self, P):
        #only allow A-Z, a-z, 0-9, and common symbols
        return all(c.isalnum() or c in '!@#$%^&*()_-+=[]{}\\|;:\'",.<>?/' for c in P)

    def signup(self):
        if self.username_input.get().isspace() or self.username_input.get() in ["Username",""]:
            messagebox.showerror("Error", "Field above can not be blank!")
        else:
            if self.password_input.get().isspace() or self.password_input.get() in ["Password",""]:
                messagebox.showerror("Error", "Field above can not be blank!")
            else:
                if not self.confirm_password_input.get() == self.password_input.get():
                    messagebox.showerror("Error", "Passwords dont match")
                else:


                    Auth.username = self.username_input.get()
                    Auth.password = self.password_input.get()
                    Auth.username_stored = self.username_input.get()
                    Auth.username_stored_value = True
                    Auth.password_input_value = True
                    messagebox.showinfo("Success","signup successful!")
                    self.master.login_screen = Login_screen(self.master)
                    self.master.login_screen.initialize_obj()
    

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

        self.master.login_screen = Login_screen(self.master)
        self.master.login_screen.initialize_obj()

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
        self.max = 800
        self.size = 100
        self.height = 4
        self.width = 9 

    def initialize_obj(self):
        #clears any widgets
        for widgets in self.master.login_frame.winfo_children():
            widgets.destroy()
        window.attributes('-fullscreen',True)
        self.master.login_frame.pack_forget()
        self.master.signup_frame.pack_forget()
        self.master.desktop_frame.pack(fill=BOTH, expand=True)


        #wallpaper
        self.photo = ImageTk.PhotoImage(Image.open(os.path.join(Variables.desktop_files, "download.png")))
        self.desktop = tk.Canvas(self.master.desktop_frame, bg="black", highlightthickness=0)
        self.desktop.pack(side=LEFT,fill=BOTH, expand=True)
        self.desktop.create_image(0, 0, image = self.photo, anchor = NW)

        #taskbar
        taskbar = tk.Canvas(self.desktop,height=100,bg="black", highlightthickness=0)
        taskbar.pack(side=BOTTOM,fill=X)

        #start button
        self.start_button = tk.Button(taskbar,bg="grey", width=5,height=2,relief='solid',highlightthickness=0,command=self.show_start_menu)
        self.start_button.pack(side=LEFT)

        #file explorer
        self.file_explorer = tk.Button(taskbar,bg="grey", width=5,height=2,relief='solid',highlightthickness=0,command= lambda: subprocess.call(["python", Variables.file_explorer]))
        self.file_explorer.pack(side=LEFT)


        self.file_explorer.bind("<Leave>", self.file_on_leave)
        self.file_explorer.bind("<Enter>", self.file_on_enter)
        self.start_button.bind("<Leave>", self.on_leave)
        self.start_button.bind("<Enter>", self.on_enter)
        
        #icons
        self.icon_size(self.max, self.size, self.height, self.width)
        self.place_icons()
        
        #----------------------------------------Work in progress (context menu)--------------------------------------------------------------------

        #makes the right click menu on desktop
        self.desktop_menu = tk.Menu(self.master.desktop_frame, tearoff=0)
        self.desktop_submenu = tk.Menu(self.master.desktop_frame, tearoff=0)


        #view sub menu
        self.desktop_submenu.add_command(label="Large icons", command=lambda: self.icon_size(800,100,4,9))
        self.desktop_submenu.add_command(label="Medium icons", command=lambda: self.icon_size(900,75,3,7))
        self.desktop_submenu.add_command(label="Small icons", command=lambda: self.icon_size(900,50,2,5))
        self.desktop_submenu.add_separator()
        self.desktop_submenu.add_command(label="Auto Arrange icons")
        self.desktop_submenu.add_command(label="Align icons to grid")
        self.desktop_submenu.add_separator()
        self.desktop_submenu.add_command(label="Show desktop icons")


        #main menu
        self.desktop_menu.add_cascade(label='View', menu=self.desktop_submenu)
        self.desktop_menu.add_command(label="Sort by")
        self.desktop_menu.add_command(label="Refresh", command=self.place_icons)
        self.desktop_menu.add_separator()
        self.desktop_menu.add_command(label="Paste")
        self.desktop_menu.add_command(label="Paste shortcut")
        self.desktop_menu.add_separator()
        self.desktop_menu.add_command(label="New",command=self.do_popup)
        self.desktop_menu.add_separator()
        self.desktop_menu.add_command(label="Display Settings")
        self.desktop_menu.add_command(label="Personalize")


        #disabled menu options
        self.desktop_menu.entryconfig("View", state="normal")
        self.desktop_menu.entryconfig("Sort by", state="disabled")
        self.desktop_menu.entryconfig("Refresh", state="normal")

        self.desktop_menu.entryconfig("Paste", state="disabled")
        self.desktop_menu.entryconfig("Paste shortcut", state="disabled")

        self.desktop_menu.entryconfig("New", state="disabled")

        self.desktop_menu.entryconfig("Display Settings", state="disabled")
        self.desktop_menu.entryconfig("Personalize", state="disabled")

        self.desktop.bind("<Button-3>", self.do_popup)

        #start button context menu
        self.start_menu = tk.Menu(self.master.desktop_frame, tearoff=0)
        self.start_menu.add_command(label="Option 1", command=lambda: print("Option 1 selected"))
        self.start_menu.add_command(label="Option 2", command=lambda: print("Option 2 selected"))
        self.start_menu.add_separator()
        self.start_menu.add_command(label="Exit", command=self.master.desktop_frame.quit)

    def show_start_menu(self):
        x, y = self.start_button.winfo_rootx(), self.start_button.winfo_rooty()
        self.start_menu.post(x, y)

    def on_leave(self,e):
        self.start_button['background'] = 'dark grey'

    #hightlight buttons in taskbar when clicked
    def on_enter(self, e):
        self.start_button['background'] = 'grey'

    def file_on_leave(self,e):
        self.file_explorer['background'] = 'dark grey'

    #hightlight buttons in taskbar when clicked
    def file_on_enter(self, e):
        self.file_explorer['background'] = 'grey'

    #sub menus
    def do_popup(self, event):
        try:
            self.desktop_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.desktop_menu.grab_release()

    #round to 150
    def ceil_150(self, num):
        ans = math.ceil(num/150)
        return (ans * 100) + (ans * 50)

    def floor_150(self, num):
        ans = math.floor(num/150)
        return (ans * 100) + (ans * 50)

    def round_150(self,num):
        c = self.ceil_150(num)
        f = self.floor_150(num)

        diff_c = c - num
        diff_f = num - f

        if diff_c <= diff_f:
            return c

        if diff_f < diff_c:
            return f


    def icon_size(self, max, size, height, width):
        self.icon_max = max
        self.icon_numsize = size
        self.icon_height = height
        self.icon_width = width
        self.place_icons()

    #places the icons
    def place_icons(self):
        for button in self.desktop.winfo_children():
            if isinstance(button, tk.Button):
                button.destroy()

        icon_y = 0
        icon_x = 0
        for files in Variables.desktop_list:
        
            file_icon = tk.Button(self.desktop, text=files, width=self.icon_width,height=self.icon_height)
            file_icon.place(x=icon_x,y=icon_y)
            if icon_y > self.icon_max:
                icon_y = -1*self.icon_numsize
                icon_x += self.icon_numsize
            icon_y += self.icon_numsize


            file_icon.bind('<B1-Motion>',lambda e, b=file_icon: self.move_icon(e, b))
            file_icon.bind('<ButtonRelease-1>',lambda e, b=file_icon: self.icon_place(e, b))

    def move_icon(self, event, file_icon):
        file_icon.place(x=window.winfo_pointerx()-self.icon_numsize/3,y=window.winfo_pointery()-self.icon_numsize/3)
    
    def icon_place(self, event, file_icon):
        self.file_icon = event.widget
        self.x = event.x
        self.y = event.y
        grid_x = event.x_root - self.x
        grid_y = event.y_root - self.y
        grid_x = (grid_x + self.icon_numsize//2)
        grid_y = (grid_y + self.icon_numsize//2)
        grid_x = (grid_x // self.icon_numsize) * self.icon_numsize
        grid_y = (grid_y // self.icon_numsize) * self.icon_numsize
        self.file_icon.place(x=grid_x, y=grid_y)
    
if __name__ == "__main__":
    window = App()
    variables = Variables()
    signup_screen = Signup_screen(window)
    window.mainloop()
