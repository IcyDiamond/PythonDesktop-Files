import tkinter as tk

class Settings:
    taskbar_hide = False
    twentyfour_hour = False
    taskbarsize = 40
    taskbar_location = "Bottom"
    menu_roundness = False
    add_blur = False
    enable_badge_var = False

class Setting_Menu():
    def __init__(self, master, parent):
        self.parent = parent
        self.window = master
        self.window.update()
        self.window.title("Taskbar Settings")

        taskbar_hide, twentyfour_hour, taskbarsize, taskbar_location, menu_roundness, add_blur, enable_badge_var = self.saved_changes()
        
        # Taskbar Hide Checkbox
        self.taskbar_hide_var = tk.BooleanVar()
        self.taskbar_hide_var.set(taskbar_hide)
        self.taskbar_hide_checkbox = tk.Checkbutton(self.window, text="Hide Taskbar", variable=self.taskbar_hide_var)
        self.taskbar_hide_checkbox.pack()
        
        # 24-Hour Format Checkbox
        self.twentyfour_hour_var = tk.BooleanVar()
        self.twentyfour_hour_var.set(twentyfour_hour)
        self.twentyfour_hour_checkbox = tk.Checkbutton(self.window, text="24-Hour Format", variable=self.twentyfour_hour_var)
        self.twentyfour_hour_checkbox.pack()
        
        # Taskbar Size Entry
        self.taskbar_size_var = tk.StringVar()
        self.taskbar_size_var.set(taskbarsize)
        self.taskbar_size_label = tk.Label(self.window, text="Taskbar Size:")
        self.taskbar_size_label.pack()
        self.taskbar_size_entry = tk.Entry(self.window, textvariable=self.taskbar_size_var)
        self.taskbar_size_entry.pack()
        
        # Taskbar Location Dropdown
        self.taskbar_location_var = tk.StringVar()
        self.taskbar_location_var.set(taskbar_location)
        self.taskbar_location_label = tk.Label(self.window, text="Taskbar Location:")
        self.taskbar_location_label.pack()
        self.taskbar_location_dropdown = tk.OptionMenu(self.window, self.taskbar_location_var, "Bottom", "Top", "Left", "Right")
        self.taskbar_location_dropdown.pack()
        
        # Menu Roundness Checkbox (WIP)
        self.menu_roundness_var = tk.BooleanVar()
        self.menu_roundness_var.set(menu_roundness)
        self.menu_roundness_checkbox = tk.Checkbutton(self.window, text="Menu Roundness (WIP)", variable=self.menu_roundness_var, state=tk.DISABLED)
        self.menu_roundness_checkbox.pack()
        
        # Add Blur Checkbox (WIP)
        self.add_blur_var = tk.BooleanVar()
        self.add_blur_var.set(add_blur)
        self.add_blur_checkbox = tk.Checkbutton(self.window, text="Add Blur (WIP)", variable=self.add_blur_var, state=tk.DISABLED)
        self.add_blur_checkbox.pack()

        # Add Badge Checkbox (WIP)
        self.enable_badge_var = tk.BooleanVar()
        self.enable_badge_var.set(enable_badge_var)
        self.enable_badge_checkbox = tk.Checkbutton(self.window, text="Show Badges on Taskbar Buttons (WIP)", variable=self.add_blur_var, state=tk.DISABLED)
        self.enable_badge_checkbox.pack()
        
        # Save Button
        self.save_button = tk.Button(self.window, text="Save", command=self.save_settings)
        self.save_button.pack()
    
    def save_settings(self):
        Settings.taskbar_hide = self.taskbar_hide_var.get()
        Settings.twentyfour_hour = self.twentyfour_hour_var.get()
        Settings.taskbarsize = int(self.taskbar_size_var.get())
        Settings.taskbar_location = self.taskbar_location_var.get()
        Settings.menu_roundness = self.menu_roundness_var.get()
        Settings.add_blur = self.add_blur_var.get()
        
        # Process the settings or save them to a file
        
        self.window.destroy()
        self.parent.refresh_taskbar_pass()

    def saved_changes(self):
        try:
            taskbar_hide = Settings.taskbar_hide
            twentyfour_hour = Settings.twentyfour_hour
            taskbarsize = Settings.taskbarsize
            taskbar_location = Settings.taskbar_location
            menu_roundness = Settings.menu_roundness
            add_blur = Settings.add_blur
            enable_badge_var = Settings.enable_badge_var
            return taskbar_hide, twentyfour_hour, taskbarsize, taskbar_location, menu_roundness, add_blur, enable_badge_var
        except:
            taskbar_hide = False
            twentyfour_hour = False
            taskbarsize = 40
            taskbar_location = "Bottom"
            menu_roundness = False
            add_blur = False
            enable_badge_var = False
            return taskbar_hide, twentyfour_hour, taskbarsize, taskbar_location, menu_roundness, add_blur, enable_badge_var
