from tkinter.constants import *
from PIL import Image, ImageTk
from tkinter import PhotoImage
from tkinter import messagebox
import customtkinter
import tkinter as tk
import subprocess
import json
import os


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("300x400")
        self.title("Python Desktop")
        self.login_frame = customtkinter.CTkFrame(self)
        self.signup_frame = customtkinter.CTkFrame(self)
        self.desktop_frame = tk.Frame(self)
        self.login_frame.grid_propagate(0)
        self.signup_frame.grid_propagate(0)
        self.desktop_frame.grid_propagate(0)
        self.login_screen = Login_screen(self)

class Variables:
    def __init__(self):
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.desktop_files = os.path.dirname(os.path.abspath(__file__))
        self.users = os.path.join(self.desktop_files, "users")
        self.file_explorer = os.path.join(self.desktop_files, "FileExplorer.py")
        self.file_temp_icon = os.path.join(self.current_directory, "image.png")
        self.desktop_list = os.listdir(self.users)
    
    def refresh_var(self):
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.desktop_files = os.path.dirname(os.path.abspath(__file__))
        self.users = os.path.join(self.desktop_files, "users")
        self.file_explorer = os.path.join(self.desktop_files, "FileExplorer.py")
        self.file_temp_icon = os.path.join(self.desktop_files, "image.png")
        self.desktop_list = f"{self.users}\\{Auth.username}\\desktop"

class Auth:
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
            self.username_input = customtkinter.CTkEntry(self.master.login_frame,validate="key")
            self.password_input = customtkinter.CTkEntry(self.master.login_frame,validate="key")
            self.login_button = customtkinter.CTkButton(self.master.login_frame, width=16, text="Login", command=self.login)
            self.link = customtkinter.CTkLabel(self.master.login_frame, text="Need an account? S\u0332I\u0332G\u0332N\u0332 \u0332U\u0332P\u0332",font=('Helveticabold', 8), cursor="hand2")

            #places the widgets onto the screen
            self.username_input.pack()
            self.password_input.pack()
            self.login_button.pack()
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
            self.stored_check()
            self.initialized = True

    def validate(self, P):
        #only allow A-Z, a-z, 0-9, and common symbols
        return all(c.isalnum() or c in '!@#$%^&*()_-+=[]{}\\|;:\'",.<>?/' for c in P)

    #Check all the info in the inputs
    def login(self):
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
        messagebox.showinfo("Success","login successful!")
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
            self.password_input.configure(show="")
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
            self.password_input.configure(show="*")
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
        self.username_input = customtkinter.CTkEntry(self.master.signup_frame,validate="key")
        self.password_input = customtkinter.CTkEntry(self.master.signup_frame,validate="key")
        self.confirm_password_input = customtkinter.CTkEntry(self.master.signup_frame,validate="key")
        self.signup_button = customtkinter.CTkButton(self.master.signup_frame, width=16, text="SignUp", command=self.signup)
        self.link = customtkinter.CTkLabel(self.master.signup_frame, text="Already a User? L\u0332O\u0332G\u0332I\u0332N\u0332",font=('Helveticabold', 8), cursor="hand2")

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
        self.master.login_screen = Login_screen(self.master)

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
            self.password_input.configure(show="")
            self.password_input.insert(0, "Password")
            Auth.password_input_value = True

    def confirm_password_out(self,e):
        if self.confirm_password_input.index("end") == 0 or  self.confirm_password_input.get().isspace():
            self.confirm_password_input.configure(validatecommand=())
            self.confirm_password_input.configure(show="")
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
            self.password_input.configure(show="*")
            self.password_input.delete(0, "end")
            Auth.password_input_value = False

    def confirm_password_text(self,e):
        if Auth.confirm_password_input_value == True:
            self.confirm_password_input.configure(show="*")
            self.confirm_password_input.delete(0, "end")
            Auth.confirm_password_input_value = False

class Desktop_screen():
    def __init__(self, master):
        self.master = master
        self.grid=True
        self.view_icons_value = True
        self.new_folder_copy = 0
        self.menu_x = 0
        self.menu_y = 0
        self.image = "e"
        self.x = None
        self.y = None
        self.img_ref = []
        self.text_ref = []
        
        self.max = 800
        self.size = 100
        self.height = 80
        self.width = 80

    def initialize_obj(self):
        #clears any widgets
        for widgets in self.master.login_frame.winfo_children():
            widgets.destroy()
        window.attributes('-fullscreen',True)
        self.master.login_frame.pack_forget()
        self.master.signup_frame.pack_forget()
        self.master.desktop_frame.pack(fill=BOTH, expand=True)


        #wallpaper
        self.icon_photo = ImageTk.PhotoImage(Image.open(os.path.join(variables.desktop_files, "image.png")))
        self.photo = ImageTk.PhotoImage(Image.open(os.path.join(variables.desktop_files, "download.png")))
        self.desktop = tk.Canvas(self.master.desktop_frame, bg="black", highlightthickness=0)
        self.desktop.pack(side=LEFT,fill=BOTH, expand=True)
        self.desktop.create_image(0, 0, image = self.photo, anchor = NW)

        #taskbar
        taskbar = tk.Canvas(self.desktop,height=100,bg="black", highlightthickness=0)
        taskbar.pack(side=BOTTOM,fill=X)

        #start button
        self.start_button = tk.Button(taskbar,bg="grey", width=5,height=2,relief='solid',highlightthickness=0,bd=0,command=self.show_start_menu)
        self.start_button.pack(side=LEFT)

        #file explorer
        self.file_explorer = tk.Button(taskbar,bg="grey", width=5,height=2,relief='solid',highlightthickness=0,command= lambda: subprocess.call(["python", variables.file_explorer]))
        self.file_explorer.pack(side=LEFT)


        self.file_explorer.bind("<Leave>", self.file_on_leave)
        self.file_explorer.bind("<Enter>", self.file_on_enter)
        self.start_button.bind("<Leave>", self.on_leave)
        self.start_button.bind("<Enter>", self.on_enter)
        
        #icons
        self.icon_size(self.max, self.size, self.height, self.width)
        
        #----------------------------------------Work in progress (context menu)--------------------------------------------------------------------

        #makes the right click menu on desktop
        self.desktop_menu = tk.Menu(self.master.desktop_frame, tearoff=0)
        self.desktop_submenu = tk.Menu(self.master.desktop_frame, tearoff=0)

        #view sub menu
        self.large_icons_var = tk.BooleanVar()
        self.view_icons_var = tk.BooleanVar()
        self.align_grid_var = tk.BooleanVar()
        self.large_icons_var.set(True)
        self.align_grid_var.set(True)
        self.view_icons_var.set(True)
        self.desktop_submenu.add_checkbutton(label="Large icons", command=lambda: self.icon_size(800,100,80,80))
        self.desktop_submenu.add_checkbutton(label="Medium icons", command=lambda: self.icon_size(900,75,50,50))
        self.desktop_submenu.add_checkbutton(label="Small icons", command=lambda: self.icon_size(900,50,35,35))
        self.desktop_submenu.add_separator()
        self.desktop_submenu.add_command(label="Auto Arrange icons")
        self.desktop_submenu.add_checkbutton(label="Align icons to grid", command=self.align_grid)
        self.desktop_submenu.add_separator()
        self.desktop_submenu.add_checkbutton(label="Show desktop icons", command=self.veiw_icons)
        self.desktop_submenu.entryconfigure("Large icons",  variable=self.large_icons_var)
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
        self.desktop_menu.entryconfig("View", state="disabled")
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

    def new_folder(self):
        
        if self.new_folder_copy == 0:
            new_folder_name = "New Folder"
        else:
            new_folder_name = f"New Folder ({self.new_folder_copy})"
        if os.path.exists(f"{variables.users}\\{Auth.username}\\desktop\\{new_folder_name}"):
            self.new_folder_copy += 1
            self.new_folder()
            return

        os.makedirs(f"{variables.users}\\{Auth.username}\\desktop\\{new_folder_name}")
        self.file_icon = tk.Button(self.desktop, width=self.icon_width, height=self.icon_height,highlightthickness=0,state='disabled')
        self.file_icon.configure(image=self.icon_photo, compound="top")
        self.file_icon.configure(wraplength=65)
        self.file_icon.configure(text=new_folder_name[:15] + "..." if len(new_folder_name) > 15 else new_folder_name)
        self.menu_x = (self.menu_x + self.icon_numsize//2)
        self.menu_y = (self.menu_y + self.icon_numsize//2)
        self.menu_x = (self.menu_x // self.icon_numsize) * self.icon_numsize
        self.menu_y = (self.menu_y // self.icon_numsize) * self.icon_numsize
        while any(button != self.file_icon and button.winfo_x() == self.menu_x and button.winfo_y() == self.menu_y for button in self.desktop.winfo_children()):
            self.menu_x += self.icon_numsize
            self.menu_y += self.icon_numsize
        self.file_icon.place(x=self.menu_x, y=self.menu_y)
        

        self.file_icon.bind('<B1-Motion>',lambda e, b=self.file_icon: self.move_icon(e, b))
        self.file_icon.bind('<ButtonRelease-1>',lambda e: self.icon_place(e))

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
        self.menu_x = event.x_root
        self.menu_y = event.y_root
        try:
            self.desktop_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.desktop_menu.grab_release()

    def icon_size(self, max, size, height, width):
        self.icon_max = max
        self.icon_numsize = size
        self.icon_height = height
        self.icon_width = width
        self.place_icons()

    def veiw_icons(self):
        if self.view_icons_value != True:
            self.view_icons_value=True
            self.place_icons()
        else:
            self.view_icons_value=False
            for button in self.desktop.winfo_children():
                if isinstance(button, tk.Button):
                    button.destroy()

    #places the icons

    def print_all_methods(self, var):
        for m in dir(var):
            if not m.startswith("_"):
                res = getattr(var, m)
                if str(res).startswith("<bound"):
                    try:
                        res = getattr(var, m)()
                    except Exception as e:
                        res = f"ERROR: {e}"
                print(f"{m}: {res}")

    def place_icons(self):
        variables.refresh_var()
        
        for image in self.img_ref:
            self.desktop.delete(image)
        for text in self.text_ref:
            self.desktop.delete(text)

        icon_y = 50
        icon_x = 50
        self.img_ref = []
        self.text_ref = []
        for files in os.listdir(variables.desktop_list):
            
            self.simage = PhotoImage(file="C:\\Users\\Musetex\\Desktop\\Desktop\\image.png")
            self.image = self.desktop.create_image(icon_x, icon_y, image=self.simage)
            self.img_ref.append(self.simage)
            text = self.desktop.create_text(icon_x,
                                         icon_y + 30,
                                         text=files[:15] + "..." if len(files) > 15 else files,
                                         anchor="n", font=("Arial", 11))
            self.text_ref.append(text)
            
            self.desktop.tag_bind(self.image, "<Button-1>", lambda event, img=self.image, txt=text: self.on_image_press(event, img, txt))
            self.desktop.tag_bind(self.image, "<B1-Motion>", lambda event, img=self.image, txt=text: self.on_image_move(event, img, txt))
            self.desktop.tag_bind(self.image, "<ButtonRelease-1>", lambda event, img=self.image, txt=text: self.on_image_release(event, img, txt))

            if icon_y > self.icon_max:
                icon_y = 0
                icon_x += self.icon_numsize
            icon_y += self.icon_numsize

    def on_image_press(self, event, img, txt):
        self.selected_img = img
        self.desktop.configure(cursor="fleur")
        self.desktop.x = event.x
        self.desktop.y = event.y
        self.desktop.coords(img, self.x, self.y)
        self.desktop.coords(txt, self.x, self.y)

    # function to handle the move event
    def on_image_move(self, event, img, txt):
        if self.selected_img == img:
            x, y = (event.x - self.desktop.x), (event.y - self.desktop.y)
            self.desktop.move(self.selected_img, x, y)
            self.desktop.move(txt, x, y)
            self.desktop.x = event.x
            self.desktop.y = event.y

    # function to handle the release event
    def on_image_release(self, event, img, txt):
        self.desktop.configure(cursor="")
        x = int(event.x/100)*100
        y = int(event.y/100)*100
        if self.grid == False:
            return
        self.desktop.coords(img, x+50, y+50)
        self.desktop.coords(txt, x+50, y+80 )
        

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
    
    def icon_place(self, event):
        self.file_icon = event.widget
        self.x = event.x
        self.y = event.y
        grid_x = event.x_root - self.x
        grid_y = event.y_root - self.y
        if self.grid == False:
            self.file_icon.place(x=grid_x, y=grid_y)
        else:
            grid_x = (grid_x + self.icon_numsize//2)
            grid_y = (grid_y + self.icon_numsize//2)
            grid_x = (grid_x // self.icon_numsize) * self.icon_numsize
            grid_y = (grid_y // self.icon_numsize) * self.icon_numsize
            while any(button != self.file_icon and button.winfo_x() == grid_x and button.winfo_y() == grid_y for button in self.desktop.winfo_children()):
                grid_x += self.icon_numsize
                grid_y += self.icon_numsize
            self.file_icon.place(x=grid_x, y=grid_y)
        


if __name__ == "__main__":
    if not os.path.exists("Users"):
        os.mkdir("Users")
    window = App()
    variables = Variables()
    signup_screen = Signup_screen(window)
    window.mainloop()
