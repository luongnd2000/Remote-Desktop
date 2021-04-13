#
import threading
import time
# Code to check if left or right mouse buttons were pressed
import socket
import win32api
import time
#
mouse_click=''
import keyboard  # using module keyboard

class KeyBoardDetectThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        while True:
            if keyboard.read_key():
                key_board = keyboard.read_key()
                print(key_board)
                time.sleep(0.01)



# Create new threads
if __name__ == '__main__':
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    print(local_ip)
