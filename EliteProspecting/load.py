#!/usr/bin/python
import socket , sys , signal
import threading
import Tkinter as tk
import myNotebook as nb
from config import config

client = None
ltd = None
painite = None

this = sys.modules[__name__]

def plugin_prefs(parent,cmdr,is_beta):
    PADX = 10
    BUTTONX = 12	# indent Checkbuttons and Radiobuttons
    PADY = 2		# close spacing

    frame = nb.Frame(parent)
    frame.columnconfigure(1, weight=1)
    nb.Label(frame,text="Set your value and restart EDMC").grid()

    this.ltd = tk.IntVar(value=config.getint("ep_LTD"))
    this.painite = tk.IntVar(value=config.getint("ep_Painite"))



    this.ip_label = nb.Label(frame,text="Server IP")
    this.ip_label.grid(row=3, padx=PADX, sticky=tk.W)
    this.server_ip = nb.Entry(frame)
    this.server_ip.grid(row=3, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

    this.port_label = nb.Label(frame,text="Server Port")
    this.port_label.grid(row=4, padx=PADX, sticky=tk.W)
    this.server_port = nb.Entry(frame)
    this.server_port.grid(row=4, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

    nb.Label(frame).grid(sticky=tk.W) # big spacer

    nb.Checkbutton(frame, text='Search for LTD greater than', variable=this.ltd).grid(row=9, column=0, padx=PADX, pady=PADY, sticky=tk.EW)
    this.ltd_threshold = nb.Entry(frame)
    this.ltd_threshold.grid(row=9, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

    nb.Checkbutton(frame, text='Search for Painite greater than', variable=this.painite).grid(row=10, column=0, padx=PADX, pady=PADY, sticky=tk.EW)
    this.painite_threshold = nb.Entry(frame)
    this.painite_threshold.grid(row=10, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

    load_value()
    return frame

def load_value():
    ltd_t = config.get("LTD_t") or 18
    port = config.get("server_port") or 44988
    ip = config.get("server_ip") or "127.0.0.1"
    painite_t = config.get("Painite_t") or 25

    this.ltd_threshold.insert(0,ltd_t)
    this.server_port.insert(0,port)
    this.server_ip.insert(0,ip)
    this.painite_threshold.insert(0,painite_t)

def prefs_changed(cmdr,is_beta) :
    config.set("ep_LTD", this.ltd.get())
    config.set("ep_Painite", this.painite.get())
    config.set("LTD_t", this.ltd_threshold.get())
    config.set("Painite_t",this.painite_threshold.get())
    config.set("server_ip",this.server_ip.get())
    config.set("server_port",this.server_port.get())

def plugin_start3(plugin_dir):
    return plugin_start()

def plugin_start(plugin_dir):
    global client
    global ltd
    global painite

    ip = str(config.get("server_ip")) or "127.0.0.1"
    port = int(config.get("server_port")) or 44988

    if config.get("ep_LTD") :
        ltd = config.get("LTD_t") or 18
    else :
        ltd = 99
    if config.get("ep_Painite") :
        painite = config.get("Painite_t") or 25
    else :
        painite = 99



    client = Client(ip, port)
    client.start()


def journal_entry(cmdr,is_beta,system,station,entry,state):
    global client
    global painite
    global ltd
    if entry['event'] == "ProspectedAsteroid":
        print(ltd," ",painite)
        for i in entry['Materials']:
            print(i['Name'])
            print(i['Proportion'])
            if i['Name'] == "LowTemperatureDiamond" and i['Proportion'] > float(ltd) :
                msg = i['Name_Localised'] + " {:.2f}  %"
                client.sends(cmdr,msg.format(i['Proportion']))
            elif i['Name'] == "Painite" and i['Proportion'] > float(painite) :
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
        try :
            print("connecting to ",self.host)
            self.sock.connect((self.host , self.port))

        except socket.error, exc:
            print("Caught exception socket.error : %s" % exc)
            print("Error connecting")
            return

        self.sendMsg("New PLayer")
        message = self.recvMsg()
        threading.Thread(target=self.recvs).start()

    def stop(self):
        print("quitting")
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
            print(msg)
            print(msg.find("quit"))
