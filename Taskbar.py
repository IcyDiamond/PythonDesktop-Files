from BlurWindow.blurWindow import blur
from screeninfo import get_monitors
from PIL import Image,ImageTk
from menu import Startmenu
from settings import Settings
from ctypes import windll
import tkinter as tk
import time
import ctypes
import atexit
import os

# get the handle to the taskbar
h = windll.user32.FindWindowA(b'Shell_TrayWnd', None)

# hide the taskbar
windll.user32.ShowWindow(h, 0)

@atexit.register
def set_show_state():
    ctypes.windll.user32.ShowWindow(h, 9)

class Taskbar(tk.Tk):
    def __init__(self,app):
        self.app = app
        self.app.config(bg='#000000')
        self.app.update()

        self.app.new_window = tk.Toplevel(self.app)
        self.app.start = Startmenu(self.app.new_window)

        #Settings
        self.taskbar_hide_var = Settings.taskbar_hide
        self.taskbarsize = Settings.taskbarsize
        self.add_blur = Settings.add_blur
        self.taskbar_active = True
        #Settings

        self.taskbarsize += 1
        
        self.monitors = get_monitors()
        for i in range(len(self.monitors)):
            if self.monitors[i].is_primary == False:
                pass
            else:
                self.monitor_width = self.monitors[i].width
                self.monitor_height = self.monitors[i].height

        if Settings.taskbar_location == "Bottom":
            self.app.geometry(f"{self.monitor_width}x{self.taskbarsize}")
            self.app.geometry(f"+0+{self.monitor_height-self.taskbarsize}")
        if Settings.taskbar_location == "Top":
            self.app.geometry(f"{self.monitor_width}x{self.taskbarsize}")
            self.app.geometry(f"+0+0")
        if Settings.taskbar_location == "Left":
            self.app.geometry(f"{self.taskbarsize}x{self.monitor_height}")
            self.app.geometry(f"+0+0")
        if Settings.taskbar_location == "Right":
            self.app.geometry(f"{self.taskbarsize}x{self.monitor_height}")
            self.app.geometry(f"+{self.monitor_width-self.taskbarsize}+0")
        self.app.overrideredirect(1)
        self.app.attributes('-topmost',True)
        #self.attributes('-alpha', 0.95)
        
        # Raise the parent window to the top of the window stack order
        self.app.lift()

        self.obj()

    def apply_blur(self):
        if self.add_blur == False:
            return
        # Get the handle to the canvas window
        hWnd = windll.user32.GetForegroundWindow()
        blur(hWnd,hexColor="#1d1d1d",Acrylic=True,Dark=True)
    
    def obj(self):
        self.app.taskbar = tk.Canvas(self.app, background='#1d1d1d', height=40, highlightthickness=0)
        self.app.taskbar.pack(expand="true",fill=tk.BOTH)
        
        self.apply_blur()
        images_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(f"{images_dir}\\assets")
        self.img= ImageTk.PhotoImage(Image.open(os.path.join(f"{images_dir}\\StartButton.png")))
        
        start_button = self.app.taskbar.create_image(0, 0, anchor="nw", image=self.img)
        self.clock = self.app.taskbar.create_text(self.monitor_width-120, 0, text="00:00", anchor="nw",fill = "white", font=('Arial', 11, 'bold'))

        self.app.taskbar.tag_bind(start_button, "<Button-1>", self.app.start.call)
        self.app.bind("<Enter>", self.enter)
        self.app.bind("<Leave>", self.leave)
        
        self.update_clock()

    def update_clock(self):
        if Settings.twentyfour_hour == True:
            current_time = time.strftime('%H:%M')
        else:
            current_time = time.strftime('%I:%M %p')
        self.app.taskbar.itemconfig(self.clock, text=current_time)

        self.app.taskbar.after(1000, self.update_clock)

    def enter(self, event=None):
        self.app.after(10, self.taskbar_show)
    def leave(self, event=None):
        if self.taskbar_active and self.taskbar_hide_var:
            self.app.after(100, self.taskbar_hide)

    def taskbar_show(self):
        if Settings.taskbar_location == "Bottom":
            t = self.app.winfo_y()

            if t <= self.monitor_height-self.taskbarsize:
                self.taskbar_active = True
                return
            self.app.geometry(f"+0+{t-1}")
            self.app.after(3, self.taskbar_show)

        if Settings.taskbar_location == "Top":
            t = self.app.winfo_y()

            if t >= 0:
                self.taskbar_active = True
                return
            self.app.geometry(f"+0+{t+1}")
            self.app.after(3, self.taskbar_show)

        if Settings.taskbar_location == "Right":
            t = self.app.winfo_x()

            if t <= self.monitor_width-Settings.taskbarsize:
                self.taskbar_active = True
                return
            self.app.geometry(f"+{t-1}+0")
            self.app.after(3, self.taskbar_show)

        if Settings.taskbar_location == "Left":
            t = self.app.winfo_x()

            if t >= 0:
                self.taskbar_active = True
                return
            self.app.geometry(f"+{t+1}+0")
            self.app.after(3, self.taskbar_show)

    def taskbar_hide(self):
        if self.app.start.menu_movement or self.app.start.menu_active:
            self.app.after(10, self.taskbar_hide)
            return
        
        if Settings.taskbar_location == "Bottom":
            if self.taskbar_active:
                t = self.app.winfo_y()
            
                if t >=self.monitor_height-1:
                    self.taskbar_active = False
                    return
                self.app.geometry(f"+0+{t+1}")
                self.app.after(3, self.taskbar_hide)
            return
        
        if Settings.taskbar_location == "Top":
            if self.taskbar_active:
                t = self.app.winfo_y()
            
                if t <=0-Settings.taskbarsize+1:
                    self.taskbar_active = False
                    return
                self.app.geometry(f"+0+{t-1}")
                self.app.after(3, self.taskbar_hide)
            return

        if Settings.taskbar_location == "Right":
            if self.taskbar_active:
                t = self.app.winfo_x()
            
                if t >= self.monitor_width-1:
                    self.taskbar_active = False
                    return
                self.app.geometry(f"+{t+1}+0")
                self.app.after(3, self.taskbar_hide)
            return
        
        if Settings.taskbar_location == "Left":
            if self.taskbar_active:
                t = self.app.winfo_x()
            
                if t <= 0-Settings.taskbarsize+1:
                    self.taskbar_active = False
                    return
                self.app.geometry(f"+{t-1}+0")
                self.app.after(3, self.taskbar_hide)
            return

if __name__ == "__main__":
    window = Taskbar()
    window.mainloop()