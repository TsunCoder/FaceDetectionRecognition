############################################# IMPORTING ################################################
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
from tkinter_custom_button import TkinterCustomButton
import tkinter.simpledialog as tsd
import cv2, os
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time


class Window1:
    def loadwindow2(self):
        self.newwindow = tk.Toplevel()
        self.newwindow.geometry('1024x720')
        self.app = Window2(self.newwindow)


    def tick(self):
        time_string = time.strftime('%H:%M:%S')
        self.clock.config(text=time_string)
        self.clock.after(200, self.tick)

    global key
    key = ''

    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    day, month, year = date.split("-")

    mont = {'01': 'January',
            '02': 'February',
            '03': 'March',
            '04': 'April',
            '05': 'May',
            '06': 'June',
            '07': 'July',
            '08': 'August',
            '09': 'September',
            '10': 'October',
            '11': 'November',
            '12': 'December'
            }

    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry('1024x720')
        self.window.configure(background='#007700')
        self.frame1 = tk.Frame(self.window, bg="#eeeeee")
        self.frame1.place(relx=0.11, rely=0.17, relwidth=0.50, relheight=0.80)

        self.img4 = tk.PhotoImage(
            file="D:/Study/Python/FACE RECOGNITION BASED ATTENDANCE MONITORING SYSTEM/FACE RECOGNITION BASED ATTENDANCE MONITORING SYSTEM/image/logo.png")
        self.message4 = tk.Label(self.window, image=self.img4, fg="white", bg='#007700', width=100, height=100)
        self.message4.place(x=30, y=10)

        self.message3 = tk.Label(self.window, text="Face Recognition Based Attendance System", bg='#007700', width=32,
                                 height=1, font=('times', 20, ' bold '))
        self.message3.place(x=150, y=30)

        self.frame3 = tk.Frame(self.window, bg='#007700')
        self.frame3.place(relx=0.43, rely=0.09, relwidth=0.09, relheight=0.07)

        self.frame4 = tk.Frame(self.window, bg='#007700')
        self.frame4.place(relx=0.2, rely=0.09, relwidth=0.23, relheight=0.07)

        self.datef = tk.Label(self.frame4, text=self.day + "-" + self.mont[self.month] + "-" + self.year + "       |  ",
                              fg="#00CCFF", bg='#007700',
                              width=55,
                              height=1, font=('times', 15, ' bold '))
        self.datef.pack(fill='both', expand=1)

        self.clock = tk.Label(self.frame3, fg="#00CCFF", bg='#007700', width=55, height=1, font=('times', 15, ' bold '))
        self.clock.pack(fill='both', expand=1)
        self.tick()

        ###################### FRAME1 ##################################
        # ATTENDANCE #
        self.head1 = tk.Label(self.frame1, text="                       For Already Registered                       ",
                              fg="white",
                              bg="#333333", font=('times', 17, ' bold '))
        self.head1.place(x=0, y=0)

        self.lblAttendance = tk.Label(self.frame1, text="-Take Attendance ", fg="#00CCFF", font=('times', 17, ' bold '))
        self.lblAttendance.place(x=15, y=45)

        self.lblLine3 = tk.Label(self.frame1,
                                 text="---------------------------------------------------------------------------",
                                 fg="#00CCFF")
        self.lblLine3.place(x=50, y=180)
        self.tv = ttk.Treeview(self.frame1, height=10, columns=('name', 'date', 'time'))
        self.tv.column('#0', width=82)
        self.tv.column('name', width=130)
        self.tv.column('date', width=133)
        self.tv.column('time', width=133)
        self.tv.grid(row=2, column=0, padx=(10, 50), pady=(240, 0), columnspan=4)
        self.tv.heading('#0', text='ID')
        self.tv.heading('name', text='NAME')
        self.tv.heading('date', text='DATE')
        self.tv.heading('time', text='TIME')

        self.lblLine4 = tk.Label(self.frame1,
                                 text="---------------------------------------------------------------------------",
                                 fg="#00CCFF")
        self.lblLine4.place(x=50, y=470)

        self.img2 = tk.PhotoImage(
            file="D:/Study/Python/FACE RECOGNITION BASED ATTENDANCE MONITORING SYSTEM/FACE RECOGNITION BASED ATTENDANCE MONITORING SYSTEM/image/face.png")
        self.trackImg = TkinterCustomButton(master=self.frame1, bg_color="#eeeeee", fg_color="#eeeeee",
                                            width=200, height=80, corner_radius=8,
                                            text_font=('times', 15, ' bold '), image=self.img2)
        self.trackImg.place(x=150, y=90)

        self.frame2Window = TkinterCustomButton(master=self.frame1, text="Chuyen Form", command=self.loadwindow2, corner_radius=10,
                                                fg_color="#F30E0B",
                                                text_font=('arial', 14, 'bold'), width=200, height=50)
        self.frame2Window.place(x=10, y=500)

        self.quitWindow = TkinterCustomButton(master=self.frame1, text="Quit", corner_radius=10,
                                              fg_color="#F30E0B",
                                              text_font=('arial', 14, 'bold'), width=200, height=50)
        self.quitWindow.place(x=230, y=500)

        self.window.mainloop()


class Window2:
    def __init__(self):
        tk.Tk()
        self.window.geometry('1024x720')

app = Window1()
