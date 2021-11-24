import time
import tkinter as tk
from tkinter import ttk
from tkinter_custom_button import TkinterCustomButton
import datetime
import time


# Attendance window
class Window1:
    # Real time
    def tick(self):
        self.time_string = time.strftime('%H:%M:%S')
        self.clock.config(text=self.time_string)
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

    def __init__(self, master):
        self.master = master
        self.newWindow = None
        self.app = None
        self.frame = tk.Frame(self.master, bg='white')
        self.frame.place(relx=0.11, rely=0.17, relwidth=0.78, relheight=0.80)

        self.lblHeader = tk.Label(self.master, text='Hệ thống điểm danh sinh viên', fg='black',
                                  font=('calibri', 22, ' bold '), width=32, height=1)
        self.lblHeader.place(x=130, y=40)
        self.imageLogo = tk.PhotoImage(file='D:/Study/Đồ án cơ sở/FaceDetectionRecognition/image/logo.png')
        self.appLogo = tk.Label(self.master, image=self.imageLogo, width='100', height='100')
        self.appLogo.place(x=70, y=10)

        self.datef = tk.Label(self.master, text=self.day + "-" + self.mont[self.month] + "-"
                                                + self.year + "   |       ",
                              font=('calibri', 15, ' bold '))
        self.datef.place(x=200, y=80)
        self.clock = tk.Label(self.master, font=('calibri', 15, ' bold '))
        self.clock.place(x=400, y=80)
        self.tick()

        self.head1 = tk.Label(self.frame, text='Đối với sinh viên đã đăng ký',
                              fg='white', bg='#33CC99', font=('calibri', 17, ' bold '), width='48')
        self.head1.place(x=0, y=0)

        self.label1 = tk.Label(self.frame, text='Điểm danh',
                               fg='#6699FF', bg='white', font=('calibri', 17, ' bold '), width='45')
        self.label1.place(x=15, y=45)

        self.lblLine = tk.Label(self.frame,
                                text="--------------------------------------------------------------------------------",
                                fg="#00CCFF", bg="white")
        self.lblLine.place(x=80, y=180)

        self.imageAttendance = tk.PhotoImage(file='D:/Study/Đồ án cơ sở/FaceDetectionRecognition/image/face.png')
        self.buttonAttendance = TkinterCustomButton(master=self.frame, bg_color='white', fg_color='white', width=100,
                                                    height=80, corner_radius=8, image=self.imageAttendance)
        self.buttonAttendance.place(x=239, y=90)

        style = ttk.Style()
        self.tvStudents = ttk.Treeview(self.frame, height='10', columns=('name', 'date', 'time'))
        style.configure(self.frame, background='white', foreground='black', fieldbackground='silver')
        style.theme_use("default")
        self.tvStudents.column('#0', width=82)
        self.tvStudents.column('name', width=130)
        self.tvStudents.column('date', width=133)
        self.tvStudents.column('time', width=133)
        self.tvStudents.grid(row=2, column=0, padx=(42, 50), pady=(230, 0), columnspan=4)
        self.tvStudents.heading('#0', text='ID')
        self.tvStudents.heading('name', text='Họ tên sinh viên')
        self.tvStudents.heading('date', text='Ngày')
        self.tvStudents.heading('time', text='Giờ')
        self.lblNoRegister = tk.Label()
        self.buttonGetInformation = TkinterCustomButton(master=self.frame, text='Đăng ký', bg_color='white', width=130,
                                                        height=40, text_font='calibri', command=self.loadWindow2,
                                                        corner_radius=8)
        self.buttonGetInformation.place(x=380, y=485)

        self.head2 = tk.Label(self.frame, text='Đối với sinh viên chưa đăng ký',
                              fg='black', bg='white', font=('calibri', 17, ' bold '))
        self.head2.place(x=40, y=490)

    def loadWindow2(self):
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.title('Đăng ký')
        self.newWindow.resizable(False, False)
        self.newWindow.geometry('720x720+380+50')
        self.app = Window2(self.newWindow)


class Window2:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master, bg='black')
        self.frame.pack()
        self.frame = tk.Frame(self.master, bg='white')
        self.frame.place(relx=0.11, rely=0.05, relwidth=0.78, relheight=0.9)
        self.head1 = tk.Label(self.frame, text='Thông tin sinh viên',
                              fg='white', bg='#33CC99', font=('calibri', 17, ' bold '), width='48')
        self.head1.place(x=0, y=0)

        # Nhập ID
        self.lblID = tk.Label(self.frame, text='Mã sinh viên:', font=('calibri', 15, ' bold '), bg='white')
        self.lblID.place(x=15, y=60)
        self.txtID = tk.Entry(self.frame, highlightthickness="2", highlightbackground="#00CCFF", width=23, fg="black",
                              font=('times', 15, ' bold '))
        self.txtID.place(x=150, y=60)
        self.clearID = TkinterCustomButton(master=self.frame, text='Clear', corner_radius=10,
                                           fg_color="#00CCFF", text_font=('arial', 10, 'bold'), width=100, height=30)
        self.clearID.place(x=420, y=60)
        # Nhập họ tên
        self.lblName = tk.Label(self.frame, text='Họ và tên:', font=('calibri', 15, ' bold '), bg='white')
        self.lblName.place(x=15, y=120)
        self.txtName = tk.Entry(self.frame, highlightthickness="2", highlightbackground="#00CCFF", width=23, fg="black",
                                font=('times', 15, ' bold '))
        self.txtName.place(x=150, y=120)
        self.clearName = TkinterCustomButton(master=self.frame, text='Clear', corner_radius=10,
                                             fg_color="#00CCFF", text_font=('arial', 10, 'bold'), width=100, height=30)
        self.clearName.place(x=420, y=120)
        self.lblLine = tk.Label(self.frame, bg='white',
                                text="---------------------------------------------------------------------------",
                                fg="#00CCFF")
        self.lblLine.place(x=100, y=180)
        # Step1
        self.lblStep1 = tk.Label(self.frame, text="Bước 1: Lấy dữ liệu khuôn mặt", fg="#00CCFF", bg='white',
                                 font=('calibri', 15, ' bold '))
        self.lblStep1.place(x=150, y=220)
        self.imageTakeImage = tk.PhotoImage(
            file='D:/Study/Đồ án cơ sở/FaceDetectionRecognition/image/photo-capture_1.png')
        self.takeImage = TkinterCustomButton(master=self.frame, bg_color="white", fg_color="white",
                                             width=200, height=80, corner_radius=8,
                                             text_font=('calibri', 15, ' bold '), image=self.imageTakeImage)
        self.takeImage.place(x=185, y=260)
        # Step2
        self.lblStep2 = tk.Label(self.frame, text="Bước 2: Lưu thông tin", fg="#00CCFF", bg='white',
                                 font=('calibri', 15, ' bold '))
        self.lblStep2.place(x=190, y=380)
        self.imageSave = tk.PhotoImage(
            file='D:/Study/Đồ án cơ sở/FaceDetectionRecognition/image/save_1.png')
        self.saveProfile = TkinterCustomButton(master=self.frame, bg_color="white", fg_color="white",
                                               width=200, height=80, corner_radius=8,
                                               text_font=('calibri', 15, ' bold '), image=self.imageSave)
        self.saveProfile.place(x=185, y=430)
        self.lblLine1 = tk.Label(self.frame, bg='white',
                                 text="---------------------------------------------------------------------------",
                                 fg="#00CCFF")
        self.lblLine1.place(x=100, y=520)


root = tk.Tk()
root.geometry('720x720+380+50')
root.resizable(False, False)
root.title('Hệ thống điểm danh sinh viên')
app = Window1(root)
root.mainloop()
