from BlurWindow.blurWindow import blur
from screeninfo import get_monitors
from PIL import Image, ImageTk
from PIL import Image,ImageTk
from settings import Settings
from menu import Startmenu
from ctypes import windll
import pygetwindow as gw
import tkinter as tk
import win32process
import subprocess
import win32gui
import win32api
import win32con
import win32ui
import ctypes
import atexit
import psutil
import time
import os
import re

# get the handle to the taskbar
h = windll.user32.FindWindowA(b'Shell_TrayWnd', None)

# hide the taskbar
windll.user32.ShowWindow(h, 0)

@atexit.register
def set_show_state():
    ctypes.windll.user32.ShowWindow(h, 9)

def toggle_app(selected_app, event=None):
    window = gw.getWindowsWithTitle(selected_app)[0]
    if window.isMaximized:
        window.minimize()
    else:
        window.maximize()
        window.activate()

class ToolTip:
    def __init__(self, app, widget, text,):
        self.app = app
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.monitors = get_monitors()
        for i in range(len(self.monitors)):
            if self.monitors[i].is_primary == False:
                pass
            else:
                self.monitor_width = self.monitors[i].width
                self.monitor_height = self.monitors[i].height
        self.app.taskbar.tag_bind(widget, "<Enter>", self.enter)
        self.app.taskbar.tag_bind(widget, "<Leave>", self.leave)
        self.app.taskbar.tag_bind(widget, "<Button-1>", lambda event, app=text: toggle_app(app))

    def enter(self, event):
        x = event.x
        self.tooltip = tk.Toplevel()
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x-25}+{self.monitor_height-60}")
        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def leave(self, _):
        if self.tooltip:
            self.tooltip.destroy()

    def __del__(self):
        if self.tooltip:
            self.tooltip.destroy()

class Taskbar(tk.Tk):
    def __init__(self, app, parent):
        self.parent = parent
        self.app = app
        self.app.config(bg='#000000')
        self.app.update()
        self.taskbar_icons = []

        self.app.new_window = tk.Toplevel(self.app)
        self.app.start = Startmenu(self.app.new_window, self)

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

        self.initialize_icon()

    def initialize_icon(self):
        self.app.taskbar = tk.Canvas(self.app, background='#1d1d1d', height=40, highlightthickness=0)
        self.app.taskbar.pack(expand="true",fill=tk.BOTH)
        
        self.apply_blur()
        images_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(f"{images_dir}\\assets")
        self.img= ImageTk.PhotoImage(Image.open(os.path.join(f"{images_dir}\\StartButton.png")))
        self.app_icon= ImageTk.PhotoImage(Image.open(os.path.join(f"{images_dir}\\GenericApp.png")))

        
        start_button = self.app.taskbar.create_image(0, 0, anchor="nw", image=self.img)
        self.clock = self.app.taskbar.create_text(self.monitor_width-120, 0, text="00:00", anchor="nw",fill = "white", font=('Arial', 11, 'bold'))

        self.app.taskbar.tag_bind(start_button, "<Button-1>", self.app.start.call)
        self.app.bind("<Enter>", self.enter)
        self.app.bind("<Leave>", self.leave)
        
        self.update_clock()
        self.set_taskbar_icons()

    def get_all_apps(self):
        all_windows = gw.getAllWindows()

        all_apps = []

        for win in all_windows:
            if not any([win.isActive, win.isMaximized, win.isMinimized]):
                continue
            all_apps.append(win)

        return all_apps

    def get_app_path(self, window):
        try:
            hwnd = window._hWnd
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            return process.exe()
        except psutil.NoSuchProcess:
            return None
        
    def get_icon(self, path):
        ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYICON)

        # Extract the large system icon
        try:
            large, small = win32gui.ExtractIconEx(path, 0)

            # Create a compatible device context
            hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
            hbmp = win32ui.CreateBitmap()
            hbmp.CreateCompatibleBitmap(hdc, ico_x, ico_x)
            hdc = hdc.CreateCompatibleDC()

            hdc.SelectObject(hbmp)
            hdc.DrawIcon((0, 0), large[0])

            # Save the icon as a file
            hbmp.SaveBitmapFile(hdc, 'icon.ico')

            # Load the saved icon using PIL
            icon_image = Image.open('icon.ico')

            # Convert the image to RGBA format
            icon_image = icon_image.convert("RGBA")

            # Create a transparent mask by setting black pixels to transparent
            data = icon_image.getdata()
            new_data = []
            for item in data:
                # Set black pixels (RGB < 10) to transparent
                if item[0] < 10 and item[1] < 10 and item[2] < 10:
                    new_data.append((item[0], item[1], item[2], 0))  # Set alpha to 0 for black pixels
                else:
                    new_data.append(item)

            # Update the image with the transparent mask
            icon_image.putdata(new_data)

            # Convert the image to Tkinter-compatible format
            icon_tk = ImageTk.PhotoImage(icon_image)
        except IndexError:
            icon_tk = self.app_icon
        return icon_tk
        
    def set_taskbar_icons(self):
        all_apps = self.get_all_apps()
        space = 0

        for app in all_apps:
            space += 50
            app_path = self.get_app_path(app)
            if app_path:
                icon = self.get_icon(app_path)
                if icon:
                    self.taskbar_app = self.app.taskbar.create_image(space, 4, anchor="nw", image=icon)
                else:
                    self.taskbar_app = self.app.taskbar.create_image(space, 4, anchor="nw", image=self.app_icon)
            self.taskbar_icons.append((icon, self.taskbar_app))
            ToolTip(self.app, self.taskbar_app, app.title)

        self.app.taskbar.after(1000, self.refresh_icons)
        

            
    def refresh_icons(self):
        for image in self.taskbar_icons:
            tk_image, taskbar_app = image
            self.app.taskbar.delete(taskbar_app)
            self.app.taskbar.delete(tk_image)
        self.set_taskbar_icons()

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
        
    def apply_blur(self):
        if self.add_blur == False:
            return
        # Get the handle to the canvas window
        hWnd = windll.user32.GetForegroundWindow()
        blur(hWnd,hexColor="#1d1d1d",Acrylic=True,Dark=True)

    def refresh_taskbar_pass(self):
        self.parent.refresh_taskbar()
    

