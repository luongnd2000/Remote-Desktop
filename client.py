

# Socket
import socket
# Work with Image
from PIL import ImageGrab
import io
#import numpy as np
from random import randint
import pyautogui
# Thread
from threading import Thread
# PyQt5
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton, QAction, QMessageBox, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect, Qt
#import autopy
def connect(host,port):
    sock = socket.socket()
    sock.connect(host,port)
class Dekstop(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def StartThread(self):
        self.start.start()

    def ChangeImage(self):
        try:
            if len(self.ip.text()) != 0 and len(self.port.text()):
                #connect(self.ip.text(),int(self.port.text()))
                sock = socket.socket()
                sock.connect((self.ip.text(), int(self.port.text())))
                while True:
                    img = ImageGrab.grab()
                    img_bytes = io.BytesIO()
                    img.save(img_bytes, format='PNG')
                    sock.send(img_bytes.getvalue())
                    data = ""
                    data = sock.recv(9999999).decode('utf-8')
                    print("Received String: ",data)
                    arr = data.split(",")
                    print(arr)
                    if arr[2] == '':
                        pyautogui.moveTo(int(arr[0]),int(arr[1]),duration=0.25)
                    if arr[2] == "L":
                        pyautogui.click(int(arr[0]),int(arr[1]))
                    if arr[2] == "R":
                        pyautogui.click(int(arr[0]),int(arr[1]),button='right')
                    if arr[3] != '':
                        pyautogui.press(arr[3])
                    if arr[4] != 0:
                        print(int(arr[4]))
                        pyautogui.scroll(int(arr[4])*20)
                sock.close()
        except:
            print("DISCONNECTED")

    def initUI(self):
        self.pixmap = QPixmap()
        self.label = QLabel(self)
        self.label.resize(self.width(), self.height())
        self.setGeometry(QRect(pyautogui.size()[0] // 4, pyautogui.size()[1] // 4, 400, 90))
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("[CLIENT] Remote Desktop: " + str(randint(99999, 999999)))
        self.start = Thread(target=self.ChangeImage, daemon=True)
        self.btn = QPushButton(self)
        self.btn.move(5, 55)
        self.btn.resize(390, 30)
        self.btn.setText("Start Demo")
        self.btn.clicked.connect(self.StartThread)
        self.ip = QLineEdit(self)
        self.ip.move(5, 5)
        self.ip.resize(390, 20)
        self.ip.setPlaceholderText("IP")
        self.port = QLineEdit(self)
        self.port.move(5, 30)
        self.port.resize(390, 20)
        self.port.setPlaceholderText("PORT")
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Dekstop()
    ex.show()
    sys.exit(app.exec())