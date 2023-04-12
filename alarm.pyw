import tkinter as tk
from tkinter.filedialog import askopenfilename
import time
import datetime
import pygame
import re
import pystray
import os
from PIL import Image


class Alarm:
    def __init__(self):
        self.status = True


def close():
    icon.stop()
    os._exit(0)


def load_music():
    filepath = askopenfilename(filetypes=[("*.mp3", "*.mp3"),
                                          ("All files", "*.*")])
    pygame.mixer.music.load(filepath)


def play_music():
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play()


def stop_music(event):
    pygame.mixer.music.stop()


def set_alarm():
    alarm.status = not alarm.status
    status_lable['text'] = 'ON ' if alarm.status else 'OFF'


def update_time():
    current_time = time.strftime("%H:%M:%S")
    time_label.config(text=current_time)
    root.after(1000, update_time)
    if time_label['text'] == alarm_entry.get() and alarm.status:
        play_music()


def check_input(event):
    if not re.fullmatch('^[0-2]?[0-9]:[0-5][0-9]:[0-5][0-9]$', alarm_entry.get()):
        alarm_entry.delete(0, tk.END)


def paste_time(event):
    if alarm_entry.get() == '':
        current_time = datetime.datetime.now()
        alarm_entry.insert(tk.END, (current_time + datetime.timedelta(minutes=10)).strftime("%H:%M:%S"))


if __name__ == '__main__':
    alarm = Alarm()
    pygame.init()
    pygame.mixer.music.load('1.mp3')

    root = tk.Tk()
    root.resizable(width=False, height=False)
    screen_width = root.winfo_screenwidth()
    root.geometry(f'260x100+{screen_width - 300}+50')
    root.overrideredirect(True)
    root.configure(bg="black")

    image = tk.PhotoImage(file='271952.png')
    image2 = tk.PhotoImage(file='1999a.png')
    image3 = tk.PhotoImage(file='cancelbutton.png')
    image_tray = Image.open('alarm-clock-16.png')

    label_frame = tk.Frame(root, bg='black')
    entry_frame = tk.Frame(root, bg='black')
    time_label = tk.Label(label_frame, font=("Arial", 40), bg='black', fg='white')
    time_label.grid(row=0, column=0, sticky='ens')
    alarm_entry = tk.Entry(entry_frame, font=("Arial", 15), width=8, bg='black', fg='white', justify='center')
    alarm_entry.grid(row=0, column=1, sticky='w')
    status_lable = tk.Label(entry_frame, bg='black', fg='white')
    status_lable.grid(row=0, column=0, ipadx=10, sticky='ws')
    status_lable['text'] = 'ON '

    buttons_frame = tk.Frame(root, bg="black")

    button = tk.Button(buttons_frame, text='Выберите музыку', image=image, command=load_music)
    button.grid(row=0, column=0, sticky='wn')

    set_alarm_button = tk.Button(buttons_frame, height=32, text='Установите время', image=image2, command=set_alarm)
    set_alarm_button.grid(row=1, column=0, sticky='wn')

    buttons_frame.grid(row=0, column=0, padx=5, pady=12, sticky='wns')
    label_frame.grid(row=0, column=0, padx=45, sticky='ens')
    entry_frame.grid(row=0, column=0, padx=40, pady=10, sticky='esw')
    alarm_entry.bind("<Button-1>", paste_time)
    root.bind("<Button-1>", stop_music)
    alarm_entry.bind('<Return>', check_input)

    menu_l = pystray.Menu(pystray.MenuItem('Close', close))
    icon = pystray.Icon('', image_tray, menu=menu_l)
    icon.title = 'Alarm Clock'
    icon.run_detached()

    update_time()

    root.mainloop()
