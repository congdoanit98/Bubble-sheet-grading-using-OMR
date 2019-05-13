#Make by DoanBlack!

from Tkinter import *
import tkFileDialog
import PIL.Image, PIL.ImageTk
import datetime
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import cv2
import imutils
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

class App():
    def __init__(self):
        self.file1 = []
        self.dsmail = []
        self.taoroot()
        self.taobutton()
        self.date = datetime.datetime.now()
        self.date.strftime("%Y%m%d %H:%M:%S")



    def taoroot(self):
        self.root = Tk()
        self.root.geometry("1510x920")
        self.root.title("Bubble Sheet Grading Software")
    def taobutton(self):
        self.heading = Label(self.root, text = "BUBBLE SHEET GRADING SOFTWARE", bg = "grey", fg = "black",width ="190", height = "2", font="UTM 16 bold").pack()
        self.addlist = Button(self.root, text="Add List", width="15", height="2", font="16", command = self.addlist).place(x=20, y=80)
        self.choiceex = Button(self.root, text="Choose Test", width = "15", height="2", font ="16", command = self.openfile).place(x = 20, y = 170)
        self.nhapcautl = Button(self.root, text= "Import Answer",width= "15", height="2", font= "16", command = self.nhapdapan).place(x=20, y=260)
        self.chambai = Button(self.root, text= "Grade", width= "15", height="2", font= "16", command=self.chambai).place(x=20, y=350)
        self.luudiem = Button(self.root, text= "Choose Folder", width= "15", height="2", font= "16", command = self.chamnhieu).place(x=20, y=440)
        self.luudiem = Button(self.root, text="Export Point", width="15", height="2", font= "16", command = self.luubangdiem).place(x=20, y=530)
        self.guimail = Button(self.root, text= "Send Email", width= "15", height="2", font= "16", command=self.guimaildi).place(x=20, y=620)

        # can =Canvas(screen, width = 300, height = 300)
        # can.place(x=200, y=100)
        # img = PIL.ImageTk.PhotoImage(file = "001.jpg")
        # can.create_image(5,5, anchor = NW, image = img)
    def chamnhieu(self):
        self.file1 = []
        self.dsddd = tkFileDialog.askdirectory(initialdir="/home/doan/PycharmProjects", title="Select Folder", )
        #print self.dsddd
        for f in os.listdir(self.dsddd):
            self.file1.append(self.dsddd+"/"+f)
        #print self.file1
        self.openedmany = Label(self.root, text="Add List Test Sussces.").place(x=30, y=495)

    def addlist(self):
        self.dssv = tkFileDialog.askopenfilename(initialdir="/home/doan/PycharmProjects/Test", title="Add list",filetypes=(("file", ".txt"), ("all file", "*.*")))
        self.list = []
        self.coutar = 0
        f = open(self.dssv, "r")
        for i in f:
            self.list.append(i)
            self.coutar = self.coutar + 1
        f.close()
        for i in range(self.coutar):
            self.list[i] = self.list[i].split()
        #print self.list
        self.addedlist = Label(self.root, text="Add list success!").place(x=30, y=135)

    def openfile(self):
        self.file1 = []
        self.filee = tkFileDialog.askopenfilename(initialdir="/home/doan/PycharmProjects/Test", title="Choose Test", filetypes=(("pictuue",".jpg"),("all file","*.*")))
        self.file1.append(self.filee)
        self.img1= cv2.imread(self.file1[len(self.file1)-1])
        self.img1 = cv2.cvtColor(self.img1, cv2.COLOR_BGR2RGB)
        self.can =Canvas(self.root, width = 2000, height = 1000)
        self.can.place(x=230, y=80)
        self.img1 = imutils.resize(self.img1, height=800)
        self.img = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.img1))
        self.can.create_image(5,5, anchor = NW, image = self.img)
        self.opened = Label(self.root, text="Choose test success!").place(x=30, y=225)

    def nhapdapan(self):
        self.dapan = tkFileDialog.askopenfilename(initialdir="/home/doan/PycharmProjects/Test", title="Import answers", filetypes=(("file",".txt"),("all file","*.*")))
        self.ANSWER_KEY = {0:0,1:0}
        j=0
        f = open(self.dapan, "r")
        for i in f:
            self.ANSWER_KEY[j] = int(i)
            j=j+1
        f.close()
        #print self.ANSWER_KEY
        self.addedanswer = Label(self.root, text="Import answers success!").place(x=30, y=315)

    def luudiem(self,tenn, diemm):
        f = open("/home/doan/Desktop/Ketqua/result.txt", "a")
        f.write(str(tenn)+"         "+str(diemm)+"          "+str(self.date.strftime("%Y%m%d %H:%M:%S")+"\n"))
        f.close()

    def luubangdiem(self):
        duongdan = "/home/doan/Desktop/Ketqua/"+str(self.date.strftime("%Y%m%d %H:%M:%S"))
        with open("/home/doan/Desktop/Ketqua/result.txt","r") as rf:
            with open(duongdan,"w+") as wf:
                wf.write("MSSV            Score        Graded at\n")
                for line in rf:
                    wf.write(line)
        f = open("/home/doan/Desktop/Ketqua/result.txt", "w")
        f.write("")
        f.close()
        self.exportedpint = Label(self.root, text="Export point sheet success!").place(x=30, y=585)

    def timkhung(self, khungbt):
        khung = None
        if len(khungbt) > 0:
            khungbt = sorted(khungbt, key=cv2.contourArea, reverse=True)
            for a in khungbt:
                peri = cv2.arcLength(a, True)
                approx = cv2.approxPolyDP(a, 0.02 * peri, True)

                if len(approx) == 4:
                    khung = approx
                    break
        return khung

    def timkhungcham(self, baithi):
        btxam = cv2.cvtColor(baithi, cv2.COLOR_BGR2GRAY)
        btmo = cv2.GaussianBlur(btxam, (5, 5), 0)
        btcanh = cv2.Canny(btmo, 75, 200)

        khungtl = cv2.findContours(btcanh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        khungtl = imutils.grab_contours(khungtl)
        return khungtl

    def timo1(self, khungtl,x):
        khung1 = None
        if len(khungtl) > 0:
            khungtl = sorted(khungtl, key=cv2.contourArea, reverse=True)
            for b in khungtl[x:30]:
                peri = cv2.arcLength(b, True)
                approx = cv2.approxPolyDP(b, 0.02 * peri, True)
                if len(approx) == 4:
                    khung1 = approx
                    break
        return khung1


    def chuyendoi(self,nhandang):
        nhandangxam = cv2.cvtColor(nhandang, cv2.COLOR_BGR2GRAY)
        nhandangmo = cv2.GaussianBlur(nhandangxam, (5, 5), 0)
        nhandangcanh = cv2.Canny(nhandangmo, 75, 200)
        khungdang = cv2.findContours(nhandangcanh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        khungdang = imutils.grab_contours(khungdang)
        return khungdang



    def tam(self, tlkhung0, thresh0):
        made = []
        n=0
        for f in tlkhung0:
            (x, y, w, h) = cv2.boundingRect(f)
            ar = w / float(h)
            if w >= 10 and h >= 10 and ar >= 0.9 and ar <= 1.1:
                made.append(f)
        made = contours.sort_contours(made, method="top-to-bottom")[0]
        for (q, i) in enumerate(np.arange(0, len(made), 10)):
            cautraloisx0 = contours.sort_contours(made[i:i + 10])[0]
            bubbled0 = None
            for (j, c) in enumerate(cautraloisx0):
                matna0 = np.zeros(thresh0.shape, dtype="uint8")
                cv2.drawContours(matna0, [c], -1, 255, -1)

                matna0 = cv2.bitwise_and(thresh0, thresh0, mask=matna0)
                tong0 = cv2.countNonZero(matna0)

                if bubbled0 is None or tong0 > bubbled0[0]:
                    bubbled0 = (tong0, j)
            n = bubbled0[1] + 1
        return n

    def luubaikt(self,fileluuu, tenluuu):
        self.baiin = cv2.cvtColor(fileluuu, cv2.COLOR_BGR2RGB)
        self.tenbailuu = str(tenluuu)+"-"+str(self.date.strftime("%Y%m%d-%H:%M:%S"))
        cv2.imwrite("/home/doan/Desktop/Ketqua/{0}.jpg".format(self.tenbailuu), self.baiin)

    def openwindow(self):
        top = Toplevel()

    def guimaildi(self):

        f = open("/home/doan/Desktop/Ketqua/result.txt", "r")
        for i in f:
            self.dsmail.append(i)
        for i in range(len(self.dsmail)):
            self.dsmail[i] = self.dsmail[i].split()
        print self.dsmail
        for i in range(len(self.dsmail)):
            for j in range(len(self.list)):
                if(self.dsmail[i][0] == self.list[j][0]):
                    tomail = self.list[j][1]
                    duongdan = "/home/doan/Desktop/Ketqua/"+self.list[j][0]+"-"+self.dsmail[j][2] +"-"+self.dsmail[j][3] + ".jpg"
                    self.sendmail(tomail, self.dsmail[i][1], duongdan)
                    print("Result was sent to "+tomail)
                    break
        f = open("/home/doan/Desktop/Ketqua/result.txt", "w")
        f.write("")
        f.close()
        self.sentmail = Label(self.root, text="Mails Were Sent.").place(x=30, y=675)

    def sendmail(self,tomail, diem,duongdan):
        email_user = 'congdoanit98@gmail.com'
        email_send = tomail
        subject = 'Score of your test!'

        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_send
        msg['Subject'] = subject

        body = 'Your score is '+diem+'. And your test was graded in below!'
        msg.attach(MIMEText(body, 'plain'))

        filename = duongdan
        attachement = open(filename, 'rb')
        namefile = os.path.basename(filename)

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachement).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= " + namefile)

        msg.attach(part)
        text = msg.as_string()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, 'congdoan')

        server.sendmail(email_user, email_send, text)
        server.quit()



    def chambai(self):
        for i in range(len(self.file1)):
            self.anh = self.file1[i]
            # self.hx = cv2.cvtColor(self.img1, cv2.COLOR_BGR2GRAY)
            # self.hm = cv2.GaussianBlur(self.hx, (5,5),0)
            # self.hc = cv2.Canny(self.hm, 75, 200)

            self.can1 = Canvas(self.root, width=2000, height=2000)
            self.can1.place(x=870, y=80)
            self.mn = cv2.imread(self.anh)

            self.hx = cv2.cvtColor(self.mn, cv2.COLOR_BGR2GRAY)
            self.hm = cv2.GaussianBlur(self.hx, (5,5),0)
            self.hc = cv2.Canny(self.hm, 75, 200)

            self.khungbt = cv2.findContours(self.hc.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            self.khungbt = imutils.grab_contours(self.khungbt)
            self.khung = None
            self.khung = self.timkhung(self.khungbt)

            self.baithi = four_point_transform(self.mn, self.khung.reshape(4, 2))

            #------
            self.khungtln = self.timkhungcham(self.baithi)
            self.khung1n = self.timo1(self.khungtln, 0)
            self.baithi = four_point_transform(self.baithi, self.khung1n.reshape(4, 2))
            #---
            self.baithi = self.baithi[20:self.baithi.shape[0] - 20, 20:self.baithi.shape[1] - 20]

            #XOAY BAI THI
            self.phantren = self.baithi[0:self.baithi.shape[0]/34, 0:self.baithi.shape[1]]
            self.row, self.col, self.cha = self.baithi.shape

            self.dem1 = 0
            for i in range(self.phantren.shape[0]):
                for j in range(self.phantren.shape[1]):
                    if self.phantren[i,j,0] <100:
                        self.dem1 = self.dem1 +1
            #print self.dem1
            if self.dem1 < 1000:
                self.dem2 = 0
                self.benphai = self.baithi[0: self.baithi.shape[0], 0: self.baithi.shape[1]/34]
                for i in range(self.benphai.shape[0]):
                    for j in range(self.benphai.shape[1]):
                        if self.benphai[i, j, 0] < 150:
                            self.dem2 = self.dem2 + 1
                #print self.dem2
                if self.dem2 < 1000:
                    self.dem3 = 0
                    self.bentrai = self.baithi[0:self.baithi.shape[0], self.baithi.shape[1]-self.baithi.shape[1]/34: self.baithi.shape[1]]
                    for i in range(self.bentrai.shape[0]):
                        for j in range(self.bentrai.shape[1]):
                            if self.bentrai[i, j, 0] < 50:
                                self.dem3 = self.dem3 + 1
                    #print self.dem3
                    if self.dem3 <1000:
                        self.r = cv2.getRotationMatrix2D((self.col/2, self.row/2),180,1)
                        self.baithi = cv2.warpAffine(self.baithi, self.r, (self.col,self.row))
                    else:
                        self.r = cv2.getRotationMatrix2D((self.col / 2, self.row / 1.488), 90, 1)
                        self.baithi = cv2.warpAffine(self.baithi, self.r, (self.row, self.col))
                else:
                    self.r = cv2.getRotationMatrix2D((self.col / 2.525, self.row / 2), -90, 1)
                    self.baithi = cv2.warpAffine(self.baithi, self.r, (self.row, self.col))

            #NHAN DANG SO CAU HOI

            self.nhandang = self.baithi[1:self.row/20, 0:self.col]
            self.khungdang = self.chuyendoi(self.nhandang)
            self.khungnhandang = self.timkhung(self.khungdang)
            self.nhandang = four_point_transform(self.nhandang, self.khungnhandang.reshape(4,2))
            self.nhandang = self.nhandang[6:self.nhandang.shape[0]-6,6:self.nhandang.shape[1]-6]

            self.phunhandang = cv2.cvtColor(self.nhandang, cv2.COLOR_BGR2GRAY)
            self.thresh0 = cv2.threshold(self.phunhandang,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            self.tlkhung0 = cv2.findContours(self.thresh0.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            self.tlkhung0 = imutils.grab_contours(self.tlkhung0)
            self.n = self.tam(self.tlkhung0,self.thresh0)
            p=0
            if self.n == 1:
                p = 10
            else:
                if self.n==2:
                    p = 15
                else:
                    p = 20

            dung = 0
            socauhoi = 0
            #ANSWER_KEY = {0:0,1:1,2:2,3:2,4:1,5:1,6:1,7:0,8:0,9:2,10: 0, 11: 0, 12: 1, 13: 2, 14: 2, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1}

            self.khungtl = self.timkhungcham(self.baithi)
            self.khung1 = self.timo1(self.khungtl,0)
            self.khung2 = self.timo1(self.khungtl, 2)

            #self.o1 = four_point_transform(self.baithi, self.khung1.reshape(4, 2))
            self.toado1 = self.khung1[0][0]
            self.d1 = (self.toado1[0] + self.toado1[1]) / 2

            for o in range(4):
                if ((self.khung1[o][0][0] + self.khung1[o][0][1]) / 2 < self.d1):
                    self.toado1 = self.khung1[o][0]
                    self.d1 = (self.toado1[0] + self.toado1[1]) / 2
            self.toado2 = self.khung2[0][0]
            self.d2 = (self.toado2[0] + self.toado2[1]) / 2
            for o in range(4):
                if ((self.khung2[o][0][0] + self.khung2[o][0][1]) / 2 < self.d2):
                    self.toado2 = self.khung2[o][0]
                    self.d2 = (self.toado2[0] + self.toado2[1]) / 2
            if (self.d1 > self.d2 ):
                self.tamp1 = self.khung1
                self.tamp2 = self.khung2
                self.toado = self.toado1
                self.toado1 = self.toado2
                self.toado2 = self.toado
            else:
                self.tamp1 = self.khung2
                self.tamp2 = self.khung1

            self.o1 = four_point_transform(self.baithi, self.tamp2.reshape(4,2))
            self.o1 = self.o1[5:self.o1.shape[0] - 5, 5:self.o1.shape[1] - 5]
            self.phukhung1 = cv2.cvtColor(self.o1, cv2.COLOR_BGR2GRAY)
            self.thresh1 = cv2.threshold(self.phukhung1, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            self.tlkhung1 = cv2.findContours(self.thresh1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            self.tlkhung1 = imutils.grab_contours(self.tlkhung1)

            cautraloi1 = []
            for f in self.tlkhung1:
                (x, y, w, h) = cv2.boundingRect(f)
                ar = w / float(h)
                if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
                    cautraloi1.append(f)

            cautraloi1 = contours.sort_contours(cautraloi1, method="top-to-bottom")[0]


            for (q, i) in enumerate(np.arange(0, len(cautraloi1), 4)):
                cautraloisx1 = contours.sort_contours(cautraloi1[i:i + 4])[0]
                bubbled1 = None

                for (j, c) in enumerate(cautraloisx1):
                    matna1 = np.zeros(self.thresh1.shape, dtype="uint8")
                    cv2.drawContours(matna1, [c], -1, 255, -1)

                    matna1 = cv2.bitwise_and(self.thresh1, self.thresh1, mask=matna1)
                    tong1 = cv2.countNonZero(matna1)

                    if bubbled1 is None or tong1 > bubbled1[0]:
                        bubbled1 = (tong1, j)
                color = (255, 0, 0)
                k = self.ANSWER_KEY[q]

                if k == bubbled1[1]:
                    color = (0, 255, 0)
                    dung += 1

                cv2.drawContours(self.o1, [cautraloisx1[k]], -1, color, 3)

            self.baithi[self.toado1[1]+5:self.toado1[1]+self.o1.shape[0]+5, self.toado1[0]+5:self.toado1[0]+self.o1.shape[1]+5] = self.o1


            self.o2 = four_point_transform(self.baithi, self.tamp1.reshape(4,2))
            self.o2 = self.o2[5:self.o2.shape[0] - 5, 5:self.o2.shape[1] - 5]
            self.phukhung2 = cv2.cvtColor(self.o2, cv2.COLOR_BGR2GRAY)
            self.thresh2 = cv2.threshold(self.phukhung2, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            self.tlkhung2 = cv2.findContours(self.thresh2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            self.tlkhung2 = imutils.grab_contours(self.tlkhung2)

            cautraloi2 = []
            for f in self.tlkhung2:
                (x, y, w, h) = cv2.boundingRect(f)
                ar = w / float(h)
                if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
                    cautraloi2.append(f)

            cautraloi2 = contours.sort_contours(cautraloi2, method="top-to-bottom")[0]

            for (q, i) in enumerate(np.arange(0, len(cautraloi2), 4)):
                cautraloisx2 = contours.sort_contours(cautraloi2[i:i + 4])[0]
                bubbled2 = None

                for (j, c) in enumerate(cautraloisx2):
                    matna2 = np.zeros(self.thresh2.shape, dtype="uint8")
                    cv2.drawContours(matna2, [c], -1, 255, -1)

                    matna2 = cv2.bitwise_and(self.thresh2, self.thresh2, mask=matna2)
                    tong2 = cv2.countNonZero(matna2)

                    if bubbled2 is None or tong2 > bubbled2[0]:
                        bubbled2 = (tong2, j)
                color = (255, 0, 0)
                k = self.ANSWER_KEY[p+q]

                if k == bubbled2[1]:
                    color = (0, 255, 0)
                    dung += 1

                cv2.drawContours(self.o2, [cautraloisx2[k]], -1, color, 3)

            self.baithi[self.toado2[1]+5:self.toado2[1]+self.o2.shape[0]+5, self.toado2[0]+5:self.toado2[0]+self.o2.shape[1]+5] = self.o2

            #print dung

            # NHAN DANG MSSV
            self.khung3 = self.timo1(self.khungtl,8)
            self.o3 = four_point_transform(self.baithi, self.khung3.reshape(4, 2))
            p = cv2.getRotationMatrix2D((self.o3.shape[0] / 2, self.o3.shape[1] / 1.52), -90, 1)
            self.o3 = cv2.warpAffine(self.o3, p, (self.o3.shape[0], self.o3.shape[1]))
            self.o3 = self.o3[5:self.o3.shape[0] - 5, 5:self.o3.shape[1] - 5]
            self.phukhung3 = cv2.cvtColor(self.o3, cv2.COLOR_BGR2GRAY)
            self.thresh3 = cv2.threshold(self.phukhung3, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            self.tlkhung3 = cv2.findContours(self.thresh3.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            self.tlkhung3 = imutils.grab_contours(self.tlkhung3)
            cautraloi3 = []
            for f in self.tlkhung3:
                (x, y, w, h) = cv2.boundingRect(f)
                ar = w / float(h)
                if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
                    cautraloi3.append(f)

            cautraloi3 = contours.sort_contours(cautraloi3, method="top-to-bottom")[0]
            mssv = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
            for (q, i) in enumerate(np.arange(0, len(cautraloi3), 10)):
                cautraloisx3 = contours.sort_contours(cautraloi3[i:i + 10])[0]
                bubbled3 = None

                for (j, c) in enumerate(cautraloisx3):
                    matna3 = np.zeros(self.thresh3.shape, dtype="uint8")
                    cv2.drawContours(matna3, [c], -1, 255, -1)

                    matna3 = cv2.bitwise_and(self.thresh3, self.thresh3, mask=matna3)
                    tong3 = cv2.countNonZero(matna3)

                    if bubbled3 is None or tong3 > bubbled3[0]:
                        bubbled3 = (tong3, j)
                mssv[q] = 9 - bubbled3[1]
            self.msv = mssv[0]
            for i in range(1, 7):
                self.msv = (self.msv * 10) + mssv[i]
            #print self.msv

            if self.n == 1:
                socauhoi = 20
            else:
                if self.n==2:
                    socauhoi = 30
                else:
                    socauhoi = 40
            self.diem = float(dung*10)/socauhoi
            #print self.diem
            cv2.putText(self.baithi, "{:.2f}".format(self.diem),(int(self.baithi.shape[0]/2.5),int(self.baithi.shape[1]/2.5)), cv2.FONT_HERSHEY_SIMPLEX,4,(255,0,0),6)
            cv2.putText(self.baithi, "{:}".format(self.msv), (int(self.baithi.shape[0] / 4.5), int(self.baithi.shape[1] / 5.2)),cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

            #self.nhandang = imutils.resize(self.nhandang, height=50)
            self.baithi = imutils.resize(self.baithi, height=800)
            #self.o2 = imutils.resize(self.o2, height=800)
            self.im = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.baithi))
            self.can1.create_image(5, 5, anchor=NW, image=self.im)


            self.luubaikt(self.baithi, self.msv)
            f = open("/home/doan/Desktop/Ketqua/result.txt", "a")
            f.write(
                str(self.msv) + "         " + str(self.diem) + "          " + str(self.date.strftime("%Y%m%d %H:%M:%S") + "\n"))
            f.close()
            self.done = Label(self.root, text="Done!").place(x=20, y=405)

    def Run(self):
        self.root.mainloop()
App().Run()
