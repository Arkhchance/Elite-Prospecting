#!/usr/bin/python
import socket , sys , signal
import threading
import Tkinter as tk
import myNotebook as nb
from config import config

#comodity
lookFor = "LowTemperatureDiamond"

#threshold
threshold = 18

#serveraddr
ip = "arkhchance.ovh"

#port
port = 44988
client = None

this = sys.modules[__name__]

def plugin_prefs(parent,cmdr,is_beta):
    this.port = tk.IntVar(value=config.get("Port"))
    frame = nb.Frame(parent)
    nb.Label(frame,text="Hello").grid()
    nb.Label(frame,text="Commander").grid()
    nb.Entry(frame,text="settings",variable=this.port).grid()

    return frame

def plugin_start(plugin_dir):
    global client
    client = Client(ip, port)
    client.start()

def journal_entry(cmdr,is_beta,system,station,entry,state):
    global client
    if entry['event'] == "ProspectedAsteroid":
        print(cmdr)
        for i in entry['Materials']:
            if i['Name'] == lookFor and i['Proportion'] > threshold :
                msg = i['Name_Localised'] + " {:.2f}  %"
                client.sends(cmdr,msg.format(i['Proportion']))

def plugin_stop():
    global client
    client.stop()


class Client():

    def __init__(self , host , port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.thread = None

    def start(self):
        self.sock.connect((self.host , self.port))
        self.sendMsg("hello")
        message = self.recvMsg()
        self.thread  = threading.Thread(target=self.recvs)
        self.thread.start()

    def stop(self):
        self.sendMsg("quit")

    def sendMsg(self  , message):
        self.sock.sendall(message.encode())

    def recvMsg(self):
        data = self.sock.recv(4096)
        return data.decode()

    def sends(self,cmdr, msg):
        message = cmdr + " : " + msg
        self.sendMsg(message)

    def recvs(self):
        while True:
            msg = self.recvMsg()
            if msg.find("quit") :
                self.sock.close()
                return
            print(msg)
