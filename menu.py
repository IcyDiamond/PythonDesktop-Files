import tkinter as tk
from screeninfo import get_monitors
from pynput.mouse import Listener
from settings import Settings
import threading
import os


class Startmenu(tk.Tk):
    def __init__(self, app):
        self.app = app

        #Settings
        self.menu_roundness = Settings.menu_roundness
        #Settings

        self.monitors = get_monitors()
        for i in range(len(self.monitors)):
            if self.monitors[i].is_primary == False:
                pass
            else:
                self.monitor_width = self.monitors[i].width
                self.monitor_height = self.monitors[i].height

        if Settings.taskbar_location == "Bottom":
            self.app.geometry("640x655")
            self.app.geometry(f"+0+{self.monitor_height}")
        if Settings.taskbar_location == "Top":
            self.app.geometry("640x655")
            self.app.geometry(f"+0+{0-655-1}")
        if Settings.taskbar_location == "Right":
            self.app.geometry("0x655")
            self.app.geometry(f"+{self.monitor_width}+0")
        if Settings.taskbar_location == "Left":
            self.app.geometry("0x655")
            self.app.geometry(f"+0+0")
        self.app.overrideredirect(1)
        self.app.attributes('-topmost',True)

        self.menu_active = False
        self.menu_movement = False
        self.side_bar_called = False
        self.side_bar_active = False

        images_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(f"{images_dir}\\assets")
        self.menu = tk.PhotoImage(file=os.path.join(f"{images_dir}\\Menu.png"))
        self.document = tk.PhotoImage(file=os.path.join(f"{images_dir}\\Document.png"))
        self.account = tk.PhotoImage(file=os.path.join(f"{images_dir}\\DefaultProfileImage.png"))
        self.photos = tk.PhotoImage(file=os.path.join(f"{images_dir}\\Images.png"))
        self.settings = tk.PhotoImage(file=os.path.join(f"{images_dir}\\Options.png"))
        self.power = tk.PhotoImage(file=os.path.join(f"{images_dir}\\Power.png"))
        self.icon_photo = tk.PhotoImage(file=os.path.join(f"{images_dir}\\UnknownIcon_Medium.png"))

        
        self.obj()
    
    def obj(self):

        self.start_menu = tk.Frame(self.app, background='#282828', width=640, height=655)
        self.start_menu.pack(expand="true",fill="both")
        self.sidebar = tk.Canvas(self.start_menu, background='#181818', width=60, height=655, highlightthickness=0)
        self.sidebar.place(anchor="nw")


        self.sidebar.bind("<Enter>", self.enter)
        self.sidebar.bind("<Leave>", self.leave)


        menu = self.sidebar.create_image(0,0,anchor="nw",image=self.menu)
        menu1 = self.sidebar.create_text(70,
                                         15,
                                         text="START"
                                         , font=("freemono bold", 16),
                                         anchor="nw",
                                         fill="white")
        self.sidebar.tag_bind(menu, "<Button-1>", self.sidebar_call)
        self.sidebar.tag_bind(menu1, "<Button-1>", self.sidebar_call)
        
        self.sidebar.create_image(0,405,anchor="nw",image=self.account)
        self.sidebar.create_text(70,
                                         420,
                                         text="Test User"
                                         , font=("Arial", 16),
                                         anchor="nw",
                                         fill="white")
        documents = self.sidebar.create_image(0,455,anchor="nw",image=self.document)
        documents1 = self.sidebar.create_text(70,
                                         470,
                                         text="Document"
                                         , font=("Arial", 16),
                                         anchor="nw",
                                         fill="white")
        self.sidebar.tag_bind(documents, "<Button-1>", lambda event=None: self.open_file(os.path.expanduser("~\\documents"), event))
        self.sidebar.tag_bind(documents1, "<Button-1>", lambda event=None: self.open_file(os.path.expanduser("~\\documents"), event))

        pictures = self.sidebar.create_image(0,505,anchor="nw",image=self.photos)
        pictures1 = self.sidebar.create_text(70,
                                         520,
                                         text="Pictures"
                                         , font=("Arial", 16),
                                         anchor="nw",
                                         fill="white")
        self.sidebar.tag_bind(pictures, "<Button-1>", lambda event=None: self.open_file(os.path.expanduser("~\\Pictures"),event))
        self.sidebar.tag_bind(pictures1, "<Button-1>", lambda event=None: self.open_file(os.path.expanduser("~\\Pictures"),event))

        self.sidebar.create_image(0,555,anchor="nw",image=self.settings)
        self.sidebar.create_text(70,
                                         570,
                                         text="Settings"
                                         , font=("Arial", 16),
                                         anchor="nw",
                                         fill="white")
        self.sidebar.create_image(0,605,anchor="nw",image=self.power)
        self.sidebar.create_text(70,
                                         620,
                                         text="Power"
                                         , font=("Arial", 16),
                                         anchor="nw",
                                         fill="white")

    def open_file(self, file, event=None):
        os.startfile(file)
        self.menu_hide()
    
    def enter(self, event=None):
        if self.menu_movement == True:
            return
        
        self.side_bar_called = True
        width = self.sidebar.winfo_width()
        self.sidebar.after(500, self.sidebar_right(width))

    def leave(self, event=None):
        if self.menu_movement == True:
            return
        
        self.side_bar_called = False
        width = self.sidebar.winfo_width()
        self.sidebar.after(100, self.sidebar_left(width))  
    
    def sidebar_right(self, t):
        if self.side_bar_called == False:
            return
        
        self.sidebar.configure(width=t)
        if t > 300:
            self.side_bar_active = True
            return
        self.app.after(1, self.sidebar_right, t+5)

    def sidebar_left(self, t):
        self.sidebar.configure(width=t)
        if t < 60:
            self.side_bar_active = False
            return
        self.app.after(1, self.sidebar_left, t-5)

    def sidebar_call(self, event=None):
        width = self.sidebar.winfo_width()
        if not self.side_bar_active:
            self.sidebar_right(width)
        else:
            self.sidebar_left(width)

    def call(self, event=None):
        x = threading.Thread(target=self.mouse)
        x.daemon = True
        x.start()

        y = threading.Thread(target=self.menu_call)
        y.daemon = True
        y.start()

    def menu_call(self, event=None):
        if not self.menu_active:
            self.menu_show()
        else:
            self.menu_hide()

    def menu_show(self):
        self.menu_movement = True

        if Settings.taskbar_location == "Bottom":
            t = self.app.winfo_y()
            if t <= self.monitor_height-655-Settings.taskbarsize:
                self.app.geometry(f"+0+{self.monitor_height-655-Settings.taskbarsize}")
                self.menu_movement = False
                self.menu_active = True
                return
        
            self.app.geometry(f"+0+{t-15}")

        if Settings.taskbar_location == "Top":
            t = self.app.winfo_y()
            if t >= 0+Settings.taskbarsize:
                self.app.geometry(f"+0+{0+Settings.taskbarsize}")
                self.menu_movement = False
                self.menu_active = True
                return
        
            self.app.geometry(f"+0+{t+15}")

        if Settings.taskbar_location == "Right":
            t = self.app.winfo_x()
            y = self.app.winfo_width()
            if t <= self.monitor_width-655-Settings.taskbarsize:
                self.app.geometry("640x655")
                self.app.geometry(f"+{self.monitor_width-Settings.taskbarsize-640}+0")
                self.menu_movement = False
                self.menu_active = True
                return
        
            self.app.geometry(f"+{t-15}+0")
            self.app.geometry(f"{y+15}x655")

        if Settings.taskbar_location == "Left":
            t = self.app.winfo_x()
            y = self.app.winfo_width()
            if t >= Settings.taskbarsize:
                self.app.geometry("640x655")
                self.app.geometry(f"+{Settings.taskbarsize}+0")
                self.menu_movement = False
                self.menu_active = True
                return
        
            self.app.geometry(f"+{t+5}+0")
            self.app.geometry(f"{y+50}x655")
        
        self.app.after(3, self.menu_show)

    def menu_hide(self):
        self.menu_movement = True
        
        if Settings.taskbar_location == "Bottom":
            t = self.app.winfo_y()
            if t >=self.monitor_height+1:
                self.app.geometry(f"+0+{self.monitor_height+1}")
                self.menu_movement = False
                self.menu_active = False
                return
            
            self.app.geometry(f"+0+{t+15}")

        if Settings.taskbar_location == "Top":
            t = self.app.winfo_y()
            if t <=0-655:
                self.app.geometry(f"+0+{0-655-1}")
                self.menu_movement = False
                self.menu_active = False
                return
            
            self.app.geometry(f"+0+{t-15}")

        if Settings.taskbar_location == "Right":
            t = self.app.winfo_x()
            y = self.app.winfo_width()
            if t >= self.monitor_width:
                self.app.geometry("0x655")
                self.app.geometry(f"+{self.monitor_width}+0")
                self.menu_movement = False
                self.menu_active = False
                return
        
            self.app.geometry(f"+{t+15}+0")
            try:
                self.app.geometry(f"{y-15}x655")
            except:
                self.app.geometry("0x655")

        if Settings.taskbar_location == "Left":
            t = self.app.winfo_x()
            y = self.app.winfo_width()
            if t <= 0:
                self.app.geometry("0x655")
                self.app.geometry(f"+-1+0")
                self.menu_movement = False
                self.menu_active = False
                return
        
            self.app.geometry(f"+{t-15}+0")
            try:
                self.app.geometry(f"{y-15}x655")
            except:
                self.app.geometry("0x655")
   
        self.app.after(3, self.menu_hide)

    def mouse(self):
        with Listener(on_click=self.on_click) as listener:
            listener.join()

    def on_click(self,x, y, button, pressed):
        if pressed:
            if y < self.app.winfo_y() or x > self.app.winfo_x()+self.app.winfo_width():
                if self.menu_active:
                    self.menu_hide()