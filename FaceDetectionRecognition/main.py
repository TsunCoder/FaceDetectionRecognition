import time
import tkinter as tk
from tkinter import ttk
from tkinter_custom_button import TkinterCustomButton
from tkinter import messagebox as mess
from tkinter import filedialog
import datetime
import time
import cv2
import os  # Thao tác tệp và thư mục
import numpy as np  # Thao tác mảng
import csv  # Đọc file
from PIL import Image, ImageTk  # Xử lý hình ảnh
import pandas as pd  # Xử lý dữ liệu


# Attendance window
class Window1:
    # Xuất excel
    def Export_Excel_Data(self):
        if len(self.tvStudents.get_children()) < 1:
            mess.showinfo("Lỗi", "Không có dữ liệu để xuất")
            return False

        self.file = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save CSV",
                                                 filetype=(("CSV File", "*.csv"), ("AllFile", "*.*")))
        with open(self.file, mode='w', newline='') as myFile:
            self.export_writer = csv.writer(myFile, delimiter='\t')
            for i in self.tvStudents.get_children():
                self.row = self.tvStudents.item(i)['values']
                self.export_writer.writerow(self.row)
            mess.showinfo("Thông báo", "Lưu thành công")

    # Kiểm tra thư mục
    def assure_path_exists(self, path):
        self.dir = os.path.dirname(path)
        if not os.path.exists(self.dir):  # Nếu không tồn tại, tự động tạo thư mục
            os.makedirs(self.dir)

    # Kiểm tra file haarcascade
    def check_haarcascadefile(self):
        self.exists = os.path.isfile("haarcascade_frontalface_default.xml")
        if self.exists:
            pass
        else:
            mess._show(title='Some file missing', message='Please contact us for help')
            root.destroy()

    # Attendance
    def TrackImage(self):
        global attendance
        # Kiểm tra tồn tại file Haar
        self.check_haarcascadefile()
        # Kiểm tra tồn tại thư mục Attendance
        self.assure_path_exists("Attendance/")
        # Kiểm tra tồn tại thư mục StudentDetails
        self.assure_path_exists("StudentDetails/")
        for k in self.tvStudents.get_children():
            self.tvStudents.delete(k)
        # Khởi tạo model LBPH
        recognizer = cv2.face.LBPHFaceRecognizer_create()

        # Kiểm tra tồn tại file Trainner.yml
        exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
        if exists3:  # Nếu có đọc file Trainner.yml
            recognizer.read("TrainingImageLabel\Trainner.yml")
        else:
            mess.showinfo('Lỗi')
            return
        # Khởi tạo file haarcascade
        haarcascadePath = "haarcascade_frontalface_default.xml"
        # Load file cascade để phát hiện khuôn mặt
        faceCascade = cv2.CascadeClassifier(haarcascadePath)

        i = 0
        # Tạo đối tượng VideoCapture để chụp video
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX  # Viết văn bản lên hình ảnh
        cols_name = ['Id', '', 'Name', '', 'Date', '', 'Time']
        # Kiểm tra file StudentDetails.csv, nếu có thì đọc file csv
        exists1 = os.path.isfile("StudentDetails\StudentDetails.csv")
        if exists1:
            df = pd.read_csv("StudentDetails\StudentDetails.csv")
        else:
            cam.release()  # Giải phóng bộ nhớ
            cv2.destroyAllWindows()
            root.destroy()
        while True:
            ret, im = cam.read()  # cam.read() trả về giá trị boolean
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)  # Chuyển đổi hình ảnh sang màu xám
            # Tìm kiếm các khuôn mặt trong hình ảnh
            faces = faceCascade.detectMultiScale(gray, 1.2, 5)
            # Vẽ một hình chữ nhật xung quanh khuôn mặt
            for (x, y, w, h) in faces:
                cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
                serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
                # So sánh khuôn mặt với dữ liệu có sẵn
                if (conf < 50):
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                    ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                    ID = str(ID)
                    ID = ID[1:-1]
                    bb = str(aa)
                    bb = bb[2:-2]
                    attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)]
                else:
                    Id = 'Unknown'
                    bb = str(Id)
                cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
            cv2.imshow('Taking Attendance', im)
            if (cv2.waitKey(1) == ord('q')):
                break
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
        exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
        if exists:
            with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
                writer = csv.writer(csvFile1)
                writer.writerow(attendance)
            csvFile1.close()
        else:
            with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
                writer = csv.writer(csvFile1)
                writer.writerow(cols_name)
                writer.writerow(attendance)
            csvFile1.close()
        with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for lines in reader1:
                i = i + 1
                if (i > 1):
                    if (i % 2 != 0):
                        iidd = str(lines[0]) + '   '
                        self.tvStudents.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
        csvFile1.close()
        cam.release()
        cv2.destroyAllWindows()

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

        self.lblHeader = tk.Label(self.master, text='Hệ thống điểm danh sinh viên', fg='#4E9F3D',
                                  font=('calibri', 22, ' bold '), width=32, height=1)
        self.lblHeader.place(x=130, y=40)
        self.imageLogo = tk.PhotoImage(file='../FaceDetectionRecognition/image/logo.png')
        self.appLogo = tk.Label(self.master, image=self.imageLogo, width='100', height='100')
        self.appLogo.place(x=70, y=10)

        self.datef = tk.Label(self.master, text=self.day + "-" + self.mont[self.month] + "-"
                                                + self.year + "   |       ",
                              font=('calibri', 15, ' bold '))
        self.datef.place(x=200, y=80)
        self.clock = tk.Label(self.master, fg='#4E9F3D', font=('calibri', 15, ' bold '))
        self.clock.place(x=400, y=80)
        self.tick()

        self.head1 = tk.Label(self.frame, text='Đối với sinh viên đã đăng ký',
                              fg='white', bg='#1E5128', font=('calibri', 17, ' bold '), width='48')
        self.head1.place(x=0, y=0)

        self.label1 = tk.Label(self.frame, text='Điểm danh',
                               fg='#4E9F3D', bg='white', font=('calibri', 17, ' bold '), width='45')
        self.label1.place(x=15, y=45)

        self.lblLine = tk.Label(self.frame,
                                text="--------------------------------------------------------------------------------",
                                fg="#1E5128", bg="white")
        self.lblLine.place(x=80, y=180)

        self.imageAttendance = tk.PhotoImage(file='../FaceDetectionRecognition/image/face.png')
        self.buttonAttendance = TkinterCustomButton(master=self.frame, command=self.TrackImage, bg_color='white',
                                                    fg_color='#D8E9A8', width=100,
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
        self.buttonGetInformation = TkinterCustomButton(master=self.frame, text='Đăng ký', fg_color='#4E9F3D',
                                                        bg_color='white', width=130,
                                                        height=40, text_font='calibri', command=self.loadWindow2,
                                                        corner_radius=8)
        self.buttonGetInformation.place(x=380, y=485)

        self.head2 = tk.Label(self.frame, text='Đối với sinh viên chưa đăng ký',
                              fg='#4E9F3D', bg='white', font=('calibri', 17, ' bold '))
        self.head2.place(x=40, y=490)

        self.menuBar = tk.Menu(self.master, relief='ridge')
        self.master.config(menu=self.menuBar)

        self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label='Xuất excel', command=self.Export_Excel_Data)
        self.menuBar.add_cascade(label='Help', menu=self.fileMenu, font=('calibri', 16, 'bold'))

    def loadWindow2(self):
        self.newWindow = tk.Toplevel(self.master)
        self.newWindow.title('Đăng ký')
        self.newWindow.resizable(False, False)
        self.newWindow.geometry('720x620+380+50')
        self.app = Window2(self.newWindow)


class Window2:
    # Xóa text
    def clearID(self):
        self.txtID.delete(0, 'end')

    def clearName(self):
        self.txtName.delete(0, 'end')

    # Kiểm tra đường dẫn thư mục
    def assure_path_exists(self, path):
        self.dir = os.path.dirname(path)
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

    # Kiểm tra file haarcascade
    def check_haarcascadefile(self):
        self.exists = os.path.isfile("haarcascade_frontalface_default.xml")
        if self.exists:
            pass
        else:
            mess._show(title='Some file missing', message='Please contact us for help')
            root.destroy()

    # Open camera
    def TakeImage(self):
        self.check_haarcascadefile()
        columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
        self.assure_path_exists("StudentDetails/")
        self.assure_path_exists("TrainingImage/")
        serial = 0
        exists = os.path.isfile("StudentDetails/StudentDetails.csv")

        if exists:
            with open("StudentDetails/StudentDetails.csv", 'r') as csvFile1:
                reader1 = csv.reader(csvFile1)
                for l in reader1:
                    serial = serial + 1
            serial = serial // 2
            csvFile1.close()
        else:
            with open("StudentDetails/StudentDetails.csv", 'a+') as csvFile1:
                writer = csv.writer(csvFile1)
                writer.writerow(columns)
                serial = 1
            csvFile1.close()
        Id = self.txtID.get()
        name = self.txtName.get()

        if ((name.isalpha()) or (' ' in name)):
            cam = cv2.VideoCapture(0)
            haarcascadefile = "haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(haarcascadefile)
            sampleNum = 0
            while (True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    sampleNum = sampleNum + 1
                    cv2.imwrite("TrainingImage/ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                                gray[y:y + h, x:x + w])
                    # display the frame
                    cv2.imshow('Taking Images', img)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                elif sampleNum > 100:
                    break
            cam.release()
            cv2.destroyAllWindows()
            row = [serial, '', Id, '', name]
            with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
        else:
            if (name.isalpha() == False):
                mess.showinfo('Lỗi', 'Vui lòng nhập đầy đủ thông tin')

    # Save
    def getImagesAndLabels(self, path):
        imagesPath = [os.path.join(path, f) for f in os.listdir(path)]

        faces = []
        Ids = []

        for imgPath in imagesPath:
            pilImage = Image.open(imgPath).convert('L')
            imageNp = np.array(pilImage, 'uint8')
            ID = int(os.path.split(imgPath)[-1].split(".")[1])
            faces.append(imageNp)
            Ids.append(ID)
        return faces, Ids

    def TrainImages(self):
        self.check_haarcascadefile()
        self.assure_path_exists("TrainingImageLabel/")
        recognizer = cv2.face_LBPHFaceRecognizer.create()
        haarcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(haarcascadePath)
        faces, ID = self.getImagesAndLabels("TrainingImage")
        try:
            recognizer.train(faces, np.array(ID))
        except:
            mess.showinfo('Thông báo', 'Chưa có dữ liệu')
            return

        recognizer.save("TrainingImageLabel/Trainner.yml")
        mess.showinfo('Thông báo', 'Lưu thành công')

    def psw(self):
        self.TrainImages()

    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master, bg='black')
        self.frame.pack()
        self.frame = tk.Frame(self.master, bg='white')
        self.frame.place(relx=0.11, rely=0.05, relwidth=0.78, relheight=0.9)
        self.head1 = tk.Label(self.frame, text='Thông tin sinh viên',
                              fg='white', bg='#1E5128', font=('calibri', 17, ' bold '), width='48')
        self.head1.place(x=0, y=0)

        # Nhập ID
        self.lblID = tk.Label(self.frame, text='Mã sinh viên:', font=('calibri', 15, ' bold '), bg='white',
                              fg='#4E9F3D')
        self.lblID.place(x=15, y=60)
        self.txtID = tk.Entry(self.frame, highlightthickness="2", highlightbackground="#D8E9A8", width=23, fg="black",
                              font=('calibri', 15, ' bold '))
        self.txtID.place(x=150, y=60)
        self.clearID = TkinterCustomButton(master=self.frame, text='Clear', command=self.clearID, corner_radius=10,
                                           fg_color="#4E9F3D", text_font=('calibri', 10, 'bold'), width=100, height=30)
        self.clearID.place(x=420, y=60)
        # Nhập họ tên
        self.lblName = tk.Label(self.frame, text='Họ và tên:', font=('calibri', 15, ' bold '), bg='white', fg='#4E9F3D')
        self.lblName.place(x=15, y=120)
        self.txtName = tk.Entry(self.frame, highlightthickness="2", highlightbackground="#D8E9A8", width=23, fg="black",
                                font=('calibri', 15, ' bold '))
        self.txtName.place(x=150, y=120)
        self.clearName = TkinterCustomButton(master=self.frame, text='Clear', command=self.clearName, corner_radius=10,
                                             fg_color="#4E9F3D", text_font=('calibri', 10, 'bold'), width=100,
                                             height=30)
        self.clearName.place(x=420, y=120)
        self.lblLine = tk.Label(self.frame, bg='white',
                                text="---------------------------------------------------------------------------",
                                fg="#1E5128")
        self.lblLine.place(x=100, y=180)
        # Step1
        self.lblStep1 = tk.Label(self.frame, text="Bước 1: Lấy dữ liệu khuôn mặt", fg="#4E9F3D", bg='white',
                                 font=('calibri', 15, ' bold '))
        self.lblStep1.place(x=150, y=220)
        self.imageTakeImage = tk.PhotoImage(
            file='../FaceDetectionRecognition/image/photo-capture_1.png')
        self.takeImage = TkinterCustomButton(master=self.frame, command=self.TakeImage, bg_color="white",
                                             fg_color="#D8E9A8",
                                             width=200, height=80, corner_radius=8,
                                             text_font=('calibri', 15, ' bold '), image=self.imageTakeImage)
        self.takeImage.place(x=185, y=260)
        # Step2
        self.lblStep2 = tk.Label(self.frame, text="Bước 2: Lưu thông tin", fg="#4E9F3D", bg='white',
                                 font=('calibri', 15, ' bold '))
        self.lblStep2.place(x=190, y=380)
        self.imageSave = tk.PhotoImage(
            file='../FaceDetectionRecognition/image/save_1.png')
        self.saveProfile = TkinterCustomButton(master=self.frame, command=self.psw, bg_color="white",
                                               fg_color="#D8E9A8",
                                               width=200, height=80, corner_radius=8,
                                               text_font=('calibri', 15, ' bold '), image=self.imageSave)
        self.saveProfile.place(x=185, y=430)
        self.lblLine1 = tk.Label(self.frame, bg='white',
                                 text="---------------------------------------------------------------------------",
                                 fg="#4E9F3D")
        self.lblLine1.place(x=100, y=520)


root = tk.Tk()
root.geometry('720x720+380+50')
root.resizable(False, False)
root.title('Hệ thống điểm danh sinh viên')
app = Window1(root)
root.mainloop()
