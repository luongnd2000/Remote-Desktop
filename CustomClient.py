import socket

from _thread import *
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
import threading
import time
# Code to check if left or right mouse buttons were pressed
import win32api
import time

mouse_click=''
key_board=''
scroll=0
class myThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
       global mouse_click
       state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
       state_right = win32api.GetKeyState(0x02)  # Right button down = 0 or 1. Button up = -127 or -128

       while True:
           a = win32api.GetKeyState(0x01)
           b = win32api.GetKeyState(0x02)

           if a != state_left:  # Button state changed
               state_left = a
               if a < 0:
                   mouse_click='L'
                   print(mouse_click)

           if b != state_right:  # Button state changed
               state_right = b
               if b < 0:
                   mouse_click = 'R'
                   print(mouse_click)
           time.sleep(0.01)
import keyboard

class KeyBoardDetectThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        global key_board
        while True:
            if keyboard.read_key():
                key_board = keyboard.read_key()
                time.sleep(0.01)



server =('192.168.1.108',999)
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
                self.desktopShow.show()
                self.desktopShow.move(0,-25)
                self.Control()
            else:
                print("not connect")
    def Control(self):
        i=1
        while True:
            global scroll
            global mouse_click
            global key_board
            img_bytes = self.sk.recv(9999999)
            time.sleep(0.01)
            self.desktopShow.ChangeImage(img_bytes)
            print('change image : ',len(img_bytes))
            data = pyautogui.position()
            send1 = str(data.x)
            send2 = str(data.y)
            data = send1 + "," + send2 + "," + mouse_click + "," + key_board + "," + str(scroll)
            print(data)
            mouse_click = ''
            key_board = ''
            scroll = 0
            if i==1:
                i=2
                self.sk.send(data.encode('utf-8'))
                self.sk.send(data.encode('utf-8'))
            else:
                self.sk.send(data.encode('utf-8'))
            time.sleep(0.01)
    def ConnectUser(self):
        if len(self.ip.text())!=0:
            connectID=self.ip.text()
            if self.ConnectStatus==False: print('try to connect user ',connectID)
            self.sk.send(connectID.encode('utf-8'))
            if self.ConnectStatus == False:
                data=self.sk.recv(9999)
                print(data.decode('utf-8'))
                if data.decode('utf-8')=='exist':
                    self.label_connected.setText('Connect status : connected ')
                    self.ConnectStatus=True
                    start_new_thread(self.SendImage,())
    def SendImage(self):
        while True:
            img = ImageGrab.grab()
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            self.sk.send(img_bytes.getvalue())
            time.sleep(0.01)
            data = ""
            data = self.sk.recv(9999999).decode('utf-8')
            print("Received String: ", data)
            arr = data.split(",")
            print(arr)
            try:
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
            except Exception:
                print("bug")
    def initUI(self):
        self.pixmap = QPixmap()
        self.label = QLabel(self)
        self.label.resize(self.width(), self.height())
        self.setGeometry(QRect(pyautogui.size()[0] // 4, pyautogui.size()[1] // 4, 400, 400))
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("Remote Desktop: ")
        #
        self.label_name = QLabel('Your UID : '+self.MyID, self)
        self.label_name.move(10,20)
        #
        self.btn = QPushButton(self)
        self.btn.move(10, 110)
        self.btn.resize(350, 30)
        self.btn.setText("Connect")
        self.btn.clicked.connect(self.ConnectUser)
        #
        self.ip = QLineEdit(self)
        self.ip.move(10, 70)
        self.ip.resize(350, 20)
        self.ip.setPlaceholderText("Enter partner UID to start Remote")
        #
        self.label_connected = QLabel('Connect status : none', self)
        self.label_connected.resize(350, 20)
        self.label_connected.move(10, 150)

class DekstopDisplay(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.initUI()
        self.move(0,-25)
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
        self.setWindowTitle("Remote Desktop")

if __name__ == '__main__':
    # Connect()
    thread1 = myThread(1, "Thread-1", 1)
    thread2 = KeyBoardDetectThread(1, "Thread-1", 1)
    # Start new Threads
    thread1.start()
    thread2.start()
    app = QApplication(sys.argv)
    desktop = DekstopDisplay()
    desktop.hide()
    desktopremote=Dekstop(desktop)
    desktopremote.show()
    sys.exit(app.exec())