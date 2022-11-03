import tkinter as tk
from PIL import ImageTk
from tkinter.constants import *
import os
import math

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        window.geometry("300x400")
        self.title("Python Desktop")
        self.login_frame = tk.Frame()
        self.signup_frame = tk.Frame()
        self.desktop_frame = tk.Frame()
        self.desktop_frame.grid_propagate(0)
        self.login_frame.grid_propagate(0)
        self.signup_frame.grid_propagate(0)

class Variables:
    wallpaper = ImageTk.PhotoImage(file = "download.png")
    desktop_files = "C:\\Users\\Musetex\\Desktop\\Desktop"
    desktop_list = os.listdir(desktop_files)

#App.signup_frame.pack()
#App.desktop_frame.pack(fill=BOTH, expand=True)

class Auth():
    username_input_value = True
    password_input_value = True
    username_stored_value = False
    password_stored_value = False
    username = ""
    password = ""
    username_stored = ""
    password_stored = ""

#login screen
class Login_screen():
    def __init__(self):
        self.initialize_obj()

    def initialize_obj(self):
        #places the login frame
        App.login_frame.pack()

        #clears any widgets
        for widgets in App.signup_frame.winfo_children():
            widgets.destroy()
        App.signup_frame.pack_forget()

        #makes all the input fields and login button
        self.username_input = tk.Entry(App.login_frame,bg="light gray")
        self.password_input = tk.Entry(App.login_frame,bg="light gray")
        self.login_button = tk.Button(App.login_frame, width=16, text="Login", command=self.login, bg="Green")
        self.link = tk.Label(App.login_frame, text="Need an account? S\u0332I\u0332G\u0332N\u0332 \u0332U\u0332P\u0332",font=('Helveticabold', 8), cursor="hand2")

        #places the widgets onto the screen
        self.username_input.pack()
        self.password_input.pack()
        self.login_button.pack()
        self.link.pack()

        #binds the buttons to a function
        self.link.bind("<Button-1>", lambda e:self.hyperlink())
        self.password_input.bind("<FocusIn>", self.password_text)
        self.username_input.bind("<FocusIn>", self.username_text)
        self.password_input.bind("<FocusOut>", self.password_out)
        self.username_input.bind("<FocusOut>", self.username_out)


    #Check all the info in the inputs
    def login(self):
        if self.username_input.get().isspace() or self.username_input.get() in ["Username",""]:
            print("Field above can not be blank!")
        else:
            if self.password_input.get().isspace() or self.password_input.get() in ["Password",""]:
                print("Field above can not be blank!")
            else:

                #Change to check info in file
                if self.username_input.get() == "username":
                    if self.password_input.get() == "password":
                        print("login successful!")
                        self.username_input_value = True
                        self.password_input_value = True
                        #desktop_screen()
                    else:
                        print("Username or Password is incorrect!")
                else:
                    print("Username or Password is incorrect!")

    
    def stored_check(self):
        if Auth.username_stored_value == True:
            self.username_input.insert(0, Auth.username_stored)
            Auth.username_stored_value = False
        else:
            self.username_input.insert(0, "Username")

        if Auth.password_stored_value == True:
            self.password_input.insert(0, Auth.password_stored)
            Auth.password_stored_value = False
        else:
            self.password_input.insert(0, "Password")
        
    def hyperlink(self):
        if self.username_input.get().isspace() or self.username_input.get() in ["Username",""]:
            Auth.username_input_value = True
        else:
            Auth.username_stored = self.username_input.get()
            Auth.username_stored_value = True

            
        if self.password_input.get().isspace() or self.password_input.get() in ["Password",""]:
            Auth.password_input_value = True
        else:
            Auth.password_stored = self.password_input.get()
            Auth.password_stored_value = True

        Signup_screen.__init__(self)
        

    #if the field is emtpy it puts the text "password"
    def password_out(self,e):
        if self.password_input.index("end") == 0 or  self.username_input.get().isspace():
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
            self.password_input.delete(0, "end")
            Auth.password_input_value = False

    #keeps the username if the user filled out that field
    def username_text(self,e):
        if Auth.username_input_value == True:
            self.username_input.delete(0, "end")
            Auth.username_input_value = False

class Signup_screen():
    def __init__(self):
        #places the signup frame
        App.signup_frame.pack()

        #clears any widgets
        for widgets in App.login_frame.winfo_children():
            widgets.destroy()
        App.login_frame.pack_forget()

        #makes all the input fields and login button
        self.username_input = tk.Entry(App.signup_frame,bg="light gray")
        self.password_input = tk.Entry(App.signup_frame,bg="light gray")
        self.signup_button = tk.Button(App.signup_frame, width=16, text="Sign Up", command=Signup_screen.signup, bg="Green")
        self.link = tk.Label(App.signup_frame, text="Already a User? L\u0332O\u0332G\u0332I\u0332N\u0332",font=('Helveticabold', 8), cursor="hand2")

        #places the widgets onto the screen
        self.username_input.pack()
        self.password_input.pack()
        self.signup_button.pack()
        self.link.pack()

        #binds the buttons to a function
        self.link.bind("<Button-1>", lambda e:self.hyperlink())
        self.password_input.bind("<FocusIn>", self.password_text)
        self.username_input.bind("<FocusIn>", self.username_text)
        self.password_input.bind("<FocusOut>", self.password_out)
        self.username_input.bind("<FocusOut>", self.username_out)


    def signup(self):
        if self.username_input.get().isspace() or self.username_input.get() in ["Username",""]:
            print("Field above can not be blank!")
        else:
            if self.password_input.get().isspace() or self.password_input.get() in ["Password",""]:
                print("Field above can not be blank!")
            else:


                Auth.username = self.username_input.get()
                Auth.password = self.password_input.get()
                Auth.username_input_value = True
                Auth.password_input_value = True
                print("signup successful!")
                Login_screen()
    

    def stored_check(self):
        if Auth.username_stored_value == True:
            self.username_input.insert(0, Auth.username_stored)
            Auth.username_stored_value = False
        else:
            self.username_input.insert(0, "Username")

        if Auth.password_stored_value == True:
            self.password_input.insert(0, Auth.password_stored)
            Auth.password_stored_value = False
        else:
            self.password_input.insert(0, "Password")


    def hyperlink(self):
        if self.username_input.get().isspace() or self.username_input.get() in ["Username",""]:
            Auth.username_input_value = True
        else:
            Auth.username_stored = self.username_input.get()
            Auth.username_stored_value = True

            
        if self.password_input.get().isspace() or self.password_input.get() in ["Password",""]:
            Auth.password_input_value = True
        else:
            Auth.password_stored = self.password_input.get()
            Auth.password_stored_value = True


        Login_screen.initialize_obj(self)


    #if the field is emtpy it puts the text "password"
    def password_out(self,e):
        if self.password_input.index("end") == 0 or  self.username_input.get().isspace():
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
            self.password_input.delete(0, "end")
            Auth.password_input_value = False

    #keeps the username if the user filled out that field
    def username_text(self,e):
        if Auth.username_input_value == True:
            self.username_input.delete(0, "end")
            Auth.username_input_value = False



#def desktop_screen():
#    #sub menus
#    def do_popup(event):
#        try:
#            desktop_menu.tk_popup(event.x_root, event.y_root)
#        finally:
#            desktop_menu.grab_release()
#
#    #round to 150
#    def ceil_150(num):
#        ans = math.ceil(num/150)
#        return (ans * 100) + (ans * 50)
#
#    def floor_150(num):
#        ans = math.floor(num/150)
#        return (ans * 100) + (ans * 50)
#
#    def round_150(num):
#        c = ceil_150(num)
#        f = floor_150(num)
#
#        diff_c = c - num
#        diff_f = num - f
#
#        if diff_c <= diff_f:
#            return c
#
#        if diff_f < diff_c:
#            return f
#
#    #hightlight buttons in taskbar when clicked
#    def on_enter(e):
#        start_button['background'] = 'Blue'
#
#    def on_leave(e):
#        start_button['background'] = 'Black'
#
#
#    class Icon:
#        max = 900
#        size = 100
#        height = 4
#        width = 9 
#
#    def icon_size(max,size,height,width):
#        Icon.icon_max = max
#        Icon.icon_numsize = size
#        Icon.icon_height = height
#        Icon.icon_width = width
#
#    #places the icons
#    def place_icons():
#        for button in desktop.winfo_children():
#            if isinstance(button, tk.Button):
#                print(button)
#                button.destroy()
#
#        icon_y = 0
#        icon_x = 0
#        icon_max ,icon_numsize, icon_height, icon_width= icon_size()
#
#        def move_icon(event, file_icon):
#            file_icon.place(x=window.winfo_pointerx()-icon_numsize/3,y=window.winfo_pointery()-icon_numsize/3)
#        
#        def icon_place(event, file_icon):
#            file_icon.place(x=round_150(window.winfo_pointerx()),y=round_150(window.winfo_pointery()))
#
#        for files in desktop_list:
#        
#            file_icon = tk.Button(desktop, text=files, width=icon_width,height=icon_height)
#            file_icon.place(x=icon_x,y=icon_y)
#            if icon_y > icon_max:
#                icon_y = -1*icon_numsize
#                icon_x += icon_numsize
#            icon_y += icon_numsize
#
#
#            file_icon.bind('<B1-Motion>',lambda e, b=file_icon: move_icon(e, b))
#            file_icon.bind('<ButtonRelease-1>',lambda e, b=file_icon: icon_place(e, b))
#
#        
#
#    for widgets in login_frame.winfo_children():
#        widgets.destroy()
#    window.attributes('-fullscreen',True)
#    login_frame.pack_forget()
#    signup_frame.pack_forget()
#
#    #Desktop
#    desktop = tk.Canvas(desktop_frame, bg="black", highlightthickness=0)
#    desktop.pack(side=LEFT,fill=BOTH, expand=True)
#    desktop.create_image(0, 0, image = wallpaper, anchor = NW)
#
#    #taskbar
#    taskbar = tk.Canvas(desktop,height=100,bg="black", highlightthickness=0)
#    taskbar.pack(side=BOTTOM,fill=X)
#
#    start_button = tk.Button(taskbar,bg="black", width=3,relief='solid',highlightthickness=0)
#    start_button.pack(side=LEFT)
#
#    start_button.bind("<Leave>", on_leave)
#    start_button.bind("<Enter>", on_enter)
#
#    #Work in progress (context menu)
#
#    #makes the right click menu on desktop
#    desktop_menu = tk.Menu(desktop_frame, tearoff=0)
#    desktop_submenu = tk.Menu(desktop_frame, tearoff=0)
#
#
#    #view sub menu
#    desktop_submenu.add_command(label="Large icons", command=lambda: Icon.icon_size(950,50,2,5))
#    desktop_submenu.add_command(label="Medium icons", command=lambda: Icon.icon_size(950,50,2,5))
#    desktop_submenu.add_command(label="Small icons", command=lambda: Icon.icon_size(950,50,2,5))
#    desktop_submenu.add_separator()
#    desktop_submenu.add_command(label="Auto Arrange icons")
#    desktop_submenu.add_command(label="Align icons to grid")
#    desktop_submenu.add_separator()
#    desktop_submenu.add_command(label="Show desktop icons")
#
#
#    #main menu
#    desktop_menu.add_cascade(label='View', menu=desktop_submenu)
#    desktop_menu.add_command(label="Sort by")
#    desktop_menu.add_command(label="Refresh", command=place_icons)
#    desktop_menu.add_separator()
#    desktop_menu.add_command(label="Paste")
#    desktop_menu.add_command(label="Paste shortcut")
#    desktop_menu.add_separator()
#    desktop_menu.add_command(label="New",command=login_screen)
#    desktop_menu.add_separator()
#    desktop_menu.add_command(label="Display Settings")
#    desktop_menu.add_command(label="Personalize")
#
#
#    #disabled menu options
#    desktop_menu.entryconfig("View", state="normal")
#    desktop_menu.entryconfig("Sort by", state="disabled")
#    desktop_menu.entryconfig("Refresh", state="normal")
#
#    desktop_menu.entryconfig("Paste", state="disabled")
#    desktop_menu.entryconfig("Paste shortcut", state="disabled")
#
#    desktop_menu.entryconfig("New", state="normal")
#
#    desktop_menu.entryconfig("Display Settings", state="disabled")
#    desktop_menu.entryconfig("Personalize", state="disabled")
#
#    desktop.bind("<Button-3>", do_popup)
#
#
#
#    place_icons()
    
if __name__ == "__main__":
    window = App()
    window.mainloop()
