import socket

from _thread import *
from pynput.mouse import Listener

# PyQt5
from PyQt5.QtGui import QPixmap, QMouseEvent, QWheelEvent
from PIL import ImageGrab
import io
from random import randint
import pyautogui
# Thread
from threading import Thread
# PyQt5
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect, Qt

server =('172.20.10.6',999)
mouse_click = ''
scroll = 0
keyboard_pressed = ''
def Send(sk,msg):
    sk.send(msg.encode('utf-8'))
def ConnectServer():
    sk=socket.socket()
    sk.connect(server)
    return sk
class Dekstop(QMainWindow):
    def __init__(self,desktopShow):
        super().__init__()
        self.ConnectStatus=False
        self.sk=ConnectServer()
        data = self.sk.recv(9999)
        self.MyID=data.decode('utf-8')
        self.initUI()
        start_new_thread(self.WaitingForConnect,())
        self.desktopShow=desktopShow
    def StartThread(self):
        start_new_thread(self.ConnectUser,())


    def WaitingForConnect(self):
        while True:
            data=self.sk.recv(9999)
            print('data from func : ',data.decode('utf-8'))
            if data.decode('utf-8')=='connected':
                print("have new connect")
                self.label_connected.setText("Connect status : Have connection")
                self.desktopShow = DekstopDisplay()
                self.Control()
            else:
                print("not connect")
    def Control(self):
        i=1
        while True:
            global scroll
            global mouse_click
            global keyboard_pressed
            img_bytes = self.sk.recv(9999999)
            self.desktopShow.ChangeImage(img_bytes)
            print('change image : ',len(img_bytes))
            data = pyautogui.position()
            send1 = str(data.x)
            send2 = str(data.y)
            data = send1 + "," + send2 + "," + mouse_click + "," + keyboard_pressed + "," + str(scroll)
            print(data)
            mouse_click = ''
            keyboard_pressed = ''
            scroll = 0
            if i==1:
                i=2
                self.sk.send(data.encode('utf-8'))
                self.sk.send(data.encode('utf-8'))
            else:
                self.sk.send(data.encode('utf-8'))
    def ConnectUser(self):
        if len(self.ip.text())!=0:
            connectID=self.ip.text()
            if self.ConnectStatus==False: print('try to connect user ',connectID)
            self.sk.send(connectID.encode('utf-8'))
            if self.ConnectStatus == False:
                data=self.sk.recv(9999)
                print(data.decode('utf-8'))
                if data.decode('utf-8')=='exist':
                    self.label_connected.setText('Connect status : connected')
                    self.ip.setPlaceholderText("Message")
                    self.btn.setText("Send Message")
                    self.ConnectStatus=True
                    while True :
                        img = ImageGrab.grab()
                        img_bytes = io.BytesIO()
                        img.save(img_bytes, format='PNG')
                        self.sk.send(img_bytes.getvalue())
                        data = ""
                        data = self.sk.recv(9999999).decode('utf-8')
                        print("Received String: ", data)
                        arr = data.split(",")
                        print(arr)
                        if arr[2] == '':
                            pyautogui.moveTo(int(arr[0]), int(arr[1]), duration=0.25)
                        if arr[2] == "L":
                            pyautogui.click(int(arr[0]), int(arr[1]))
                        if arr[2] == "R":
                            pyautogui.click(int(arr[0]), int(arr[1]), button='right')
                        if arr[3] != '':
                            pyautogui.press(arr[3])
                        if arr[4] != 0:
                            print(int(arr[4]))
                            pyautogui.scroll(int(arr[4]) * 20)
                else :
                    self.label_connected.setText('Connect status : '+data.decode('utf-8'))
    def SendMessage(self):
        if len(self.ip.text()) != 0:
            connectID = self.ip.text()
            self.sk.send(connectID.encode('utf-8'))
    def initUI(self):
        self.pixmap = QPixmap()
        self.label = QLabel(self)
        self.label.resize(self.width(), self.height())
        self.setGeometry(QRect(pyautogui.size()[0] // 4, pyautogui.size()[1] // 4, 400, 400))
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("Remote Desktop: ")
        #
        self.label_name = QLabel('Your id : '+self.MyID, self)
        #
        self.btn = QPushButton(self)
        self.btn.move(0, 60)
        self.btn.resize(390, 30)
        self.btn.setText("Connect")
        self.btn.clicked.connect(self.ConnectUser)
        #
        self.ip = QLineEdit(self)
        self.ip.move(0, 30)
        self.ip.resize(390, 20)
        self.ip.setPlaceholderText("UID")
        #
        self.label_connected = QLabel('Connect status : none', self)
        self.label_connected.resize(250, 20)
        self.label_connected.move(0, 90)

mouse_click = ''
scroll = 0
keyboard_pressed = ''
class DekstopDisplay(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def keyPressEvent(self, event):
        global keyboard_pressed
        keyboard_pressed = event.text()
        print(event.text())
    def mousePressEvent(self, event: QMouseEvent):
        global mouse_click
        if event.button() == Qt.LeftButton:
            mouse_click = "L"
        if event.button() == Qt.RightButton:
            mouse_click = "R"
    def wheelEvent(self, event: QWheelEvent) -> None:
        global scroll
        scroll = scroll+1
    def ChangeImage(self,img_bytes):
        self.pixmap.loadFromData(img_bytes)
        self.label.resize(self.width(), self.height())
        self.label.setPixmap(self.pixmap)
    def initUI(self):
        self.pixmap = QPixmap()
        self.label = QLabel(self)
        self.label.resize(self.width(), self.height())
        self.setGeometry(QRect(pyautogui.size()[0] // 4, pyautogui.size()[1] // 4, 1920, 1080))
        self.showMaximized()
        self.setWindowTitle("[SERVER] Remote Desktop: " + str(randint(99999, 999999)))

if __name__ == '__main__':
    # Connect()
    app = QApplication(sys.argv)
    desktop = DekstopDisplay()
    desktop.show()
    desktopremote=Dekstop(desktop)
    desktopremote.show()
    sys.exit(app.exec())