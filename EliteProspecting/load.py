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
    frame = nb.Frame(parent)

    this.ltd = tk.IntVar(value=config.getint("ep_LTD"))
    this.painite = tk.IntVar(value=config.getint("ep_Painite"))

    nb.Label(frame,text="Settings").grid()
    nb.Checkbutton(frame, text='Search for LTD', variable=this.ltd).grid()
    nb.Checkbutton(frame, text='Search for Painite', variable=this.painite).grid()

    return frame

def prefs_changed(cmdr,is_beta) :
    print(this.ltd.get())
    print(this.painite.get())
    config.set("ep_LTD", this.ltd.get())
    config.set("ep_Painite", this.painite.get())


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
        self.sendMsg("New PLayer")
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
