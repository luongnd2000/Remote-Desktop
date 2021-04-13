import socket
from _thread import *
import time
import win32api
from time import sleep
from PIL import Image
import io
import time
import pygame
from pygame.locals import *
from pynput.mouse import Listener
import numpy as np
from random import randint
import pyautogui
from threading import Thread
# PyQt5
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton, QAction, QMessageBox
from PyQt5.QtGui import QPixmap, QMouseEvent, QWheelEvent
from PyQt5.QtCore import QRect, Qt
ip='192.168.1.108'
port=999
UID=1
userConnected=list()
class UConnect():
    def __init__(self,uid,connect,addr):
        self.uid=uid
        self.connect=connect
        self.addr=addr
        self.connectted=False
def ListenUser(user):
    if user.connectted==False :
        print("waiting for mess from ",user.uid)
        data = user.connect.recv(9999999)
        print("Received from ",user.uid)
        data = data.decode('utf-8')
    for uc in userConnected:
        if (str(uc.uid) == data):
            mess = 'none'
            user.connect.send(mess.encode('utf-8'))
            mess='exist'
            time.sleep(0.01)
            user.connect.send(mess.encode('utf-8'))
            ConnectUser(user,uc)
    if user.connectted==False:
        mess = 'notexist'
        print("send not exit to user : ",user.uid)
        user.connect.send(mess.encode('utf-8'))
        ListenUser(user)

def ConnectUser(user1,user2):
    user1.connectted,user2.connectted=True,True
    print("Connect user ",user1.uid," vs ",user2.uid)
    user2.connect.send('connected'.encode('utf-8'))
    while True:
        #send and received screen
        data=user1.connect.recv(9999999)
        print("Received mess from user ",user1.uid," : ",len(data))
        time.sleep(0.01)
        user2.connect.send(data)
        #send and received control
        data=user2.connect.recv(9999999)
        print("Received mess from user ",user2.uid," : ",data.decode('utf-8'))
        user1.connect.send('none'.encode('utf-8'))
        time.sleep(0.01)
        user1.connect.send(data)
def InitSocket():
    global UID
    print('Started server')
    sk=socket.socket()
    sk.bind((ip,port))
    sk.listen()
    while True:
        print("Waitting for new connect...")
        conn,addr=sk.accept()
        print("Client connected : ",addr)
        uc=UConnect(UID,conn,addr)
        UID=UID+1
        #send id
        data = str(uc.uid)
        conn.send(data.encode('utf-8'))
        userConnected.append(uc)
        #thread listen
        start_new_thread(ListenUser, (uc,))
if __name__ == '__main__':
    InitSocket()