from BlurWindow.blurWindow import blur
from screeninfo import get_monitors
from PIL import Image, ImageTk
from settings import Settings
from menu import Startmenu
from ctypes import windll
import pywinctl as pwc
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
    window = pwc.getWindowsWithTitle(selected_app)[0]
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
        self.ative_tooltips = []
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
        self.ative_tooltips.append(self.tooltip)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x-25}+{self.monitor_height-60}")
        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def leave(self, _):
        if self.tooltip:
            self.tooltip.destroy()
            self.ative_tooltips.remove(self.tooltip)

    def delete(self):
        print("test")
        #for i in self.ative_tooltips:
        #    if self.tooltip:
        #        self.tooltip.destroy()
        #        self.ative_tooltips.remove(self.tooltip)

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
        self.img = ImageTk.PhotoImage(Image.open(os.path.join(f"{images_dir}\\StartButton.png")))
        self.app_icon = ImageTk.PhotoImage(Image.open(os.path.join(f"{images_dir}\\GenericApp.png")))

        self.windows = {}

        start_button = self.app.taskbar.create_image(0, 0, anchor="nw", image=self.img)
        self.clock = self.app.taskbar.create_text(self.monitor_width-120, 0, text="00:00", anchor="nw",fill = "white", font=('Arial', 11, 'bold'))

        self.app.taskbar.tag_bind(start_button, "<Button-1>", self.app.start.call)
        self.app.bind("<Enter>", self.enter)
        self.app.bind("<Leave>", self.leave)
        
        self.update_clock()
        self.auto_update()

    def auto_update(self):
        win32gui.EnumWindows(self.enum_windows, None)
        self.delete_applications()
        self.app.taskbar.after(1000, self.auto_update)
        

    def create_application(self, app_name, hwnd):
        if hwnd in self.windows:
            _, app_button = self.windows[hwnd]
            app_button.config(text=app_name)  # Update the text on the button
        else:
            app_button = tk.Button(self.app.taskbar, text=app_name, bg='black', fg='white', wraplength=80, borderwidth=0, command=lambda name=app_name: self.focus_application(name))
            app_button.place(x=(len(self.windows)*100)+60)
            print(len(self.windows)+1)
        self.windows[hwnd] = (app_name, app_button)

    def delete_applications(self):
        active_hwnds = set()
        win32gui.EnumWindows(lambda hwnd, _: active_hwnds.add(hwnd), None)
        inactive_hwnds = [hwnd for hwnd in self.windows.keys() if hwnd not in active_hwnds]
        for hwnd in inactive_hwnds:
            app_name, app_button = self.windows.pop(hwnd)
            app_button.destroy()
            
        self.windows = {hwnd: (app_name, app_button) for hwnd, (app_name, app_button) in self.windows.items() if hwnd not in inactive_hwnds}
        print(len(self.windows)+1)

    def enum_windows(self, hwnd, lParam): #Gets all opened windows and filters them
        if win32gui.IsWindowVisible(hwnd) and self.is_taskbar_window(hwnd):
            app_name = win32gui.GetWindowText(hwnd)
            if app_name and "Microsoft Text Input Application" not in app_name and "Windows Input Experience" not in app_name:
                self.create_application(app_name, hwnd)

    def is_taskbar_window(self, hwnd):
        if win32gui.GetWindow(hwnd, win32con.GW_OWNER) != 0:
            return False
        if win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) & win32con.WS_EX_TOOLWINDOW:
            return False
        return True

    def focus_application(self, app_name):
        hwnd = win32gui.FindWindow(None, app_name)
        if hwnd:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)

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

    

