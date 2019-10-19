#!/usr/bin/python
import Tkinter as tk
import socket , sys , time
import threading
from config import config

class Prospecting():
    def __init__(self):
        self.connected = False
        self.run = True
        self.parent = None
        self.total_msg  = 0
        self.messages = []
        self.colors = []
        self.total_msg_display = 6
        self.status = [None] * self.total_msg_display
        self.buffer = 1024
        self.sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.load_config()
        print(sys.version)

    def load_config(self,change = False):
        self.ip = config.get("EP_server_ip") or "127.0.0.1"
        self.port = config.get("EP_server_port") or 44988

        self.track_LTD = config.getint("EP_track_LTD")
        self.track_Painite = config.getint("EP_track_Painite")
        self.new_win = config.getint("EP_use_new_window")
        self.win_trans = config.getint("EP_win_trans")
        self.miss = config.getint("EP_miss")

        self.ltd_threshold = config.get("EP_LTD_t") or 18
        self.painite_threshold = config.get("EP_Painite_t") or 25
        self.font_size = config.get("EP_font_size") or 14

        self.my_color = config.get("EP_my_color") or "Red"
        self.color = config.get("EP_color") or "Yellow"

        self.pos_x = config.get("EP_pos_x") or 200
        self.pos_y = config.get("EP_pos_y") or 200

        if change :
            self.refresh_display()

    def init_gui(self,parent):
        self.parent = parent
        self.frame = tk.Frame(parent, borderwidth=2)
        self.frame.grid(sticky=tk.NSEW, columnspan=2)

        row = 0
        self.connection = tk.Button(self.frame, text="Connect to server", command=self.connect)
        self.connection.grid(row=row, columnspan=2)
        if self.new_win == 0:
            for i in range(self.total_msg_display):
                self.status[i] = tk.Label(self.frame, text="", foreground="yellow")
                self.status[i].config(font=("Courier", int(self.font_size)))
                row += 1
                self.status[i].grid(row=row, pady=5, sticky=tk.W)
        else :
            self.win_x = tk.Scale(self.frame, from_=1, to=6000, orient=tk.HORIZONTAL, label="x position",command=self.update_new_win)
            self.win_x.grid(row=row+3, columnspan=2)
            self.win_x.set(100)
            row += 1
            self.win_y = tk.Scale(self.frame, from_=1, to=3000, orient=tk.HORIZONTAL, label="y position",command=self.update_new_win)
            self.win_y.grid(row=row+6, columnspan=2)
            self.win_y.set(100)

            self.window = tk.Toplevel()
            if sys.platform == 'win32' and self.win_trans == 1 :
                self.window.attributes("-transparentcolor", 'black')
            self.window.wm_attributes("-topmost", True)
            self.window.overrideredirect(True)
            self.window.configure(background='black')
            self.window.wm_geometry('+' + str(439) + '+' + str(172))

            for i in range(self.total_msg_display):
                self.status[i] = tk.Label(self.window)
                self.status[i].config(font=("Courier", int(self.font_size)),background='black')
                self.status[i].pack(side="top", fill="both", expand=True, padx=10, pady=10)
                if i == 0 :
                    self.status[i]['text'] = "Waiting..."

        return self.frame

    def update_new_win(self,val):
        self.window.wm_geometry('+' + str(self.win_x.get()) + '+' + str(self.win_y.get()))

    def display_msg(self,msg,mine=True):
        if mine :
            color = "mine"
        else :
            color = "other"

        self.colors.append(color)
        self.messages.append(msg)
        self.total_msg += 1

        if self.total_msg > self.total_msg_display :
            self.messages.pop(0)
            self.colors.pop(0)
            self.total_msg -= 1

        self.refresh_display()

    def refresh_display(self):
        for i in range(len(self.messages)):
            if self.colors[i] == "mine":
                color = self.my_color
            else :
                color = self.color

            self.status[i].config(foreground=color)
            self.status[i]['text'] = self.messages[i]

    def sendMsg(self,message):
        try :
            self.sock.sendall(message.encode())
        except socket.error as e:
            print("error sending")
            print("Caught exception socket.error : %s" % e)

    def connect(self):
        try :
            self.connection["text"] = "Connecting..."
            print("connecting to ",self.ip)
            self.sock.connect((self.ip , int(self.port)))

        except socket.error as e:
            print("Caught exception socket.error : %s" % e)
            print("Error connecting")
            self.connection["text"] = "Error connecting check configuration"
            return

        self.connected = True
        self.sendMsg("New Player")
        threading.Thread(target=self.recvs).start()
        self.connection["text"] = "Connected"
        time.sleep(2)
        self.connection.grid_remove()

    def stop(self):
        config.set("EP_pos_x", self.pos_x)
        config.set("EP_pos_y", self.pos_y)
        if not self.connected:
            return
        self.run = False
        self.connected = False
        self.sendMsg("quit")
        time.sleep(1)
        try:
            self.sock.close()
        except socket.error as e:
            print("socket.error : %s" % e)

    def recvMsg(self):
        data = self.sock.recv(self.buffer)
        return data.decode()

    def recvs(self):
        while self.run:
            try:
                msg = self.recvMsg()
                if msg.decode() == "quit":
                    break
                self.display_msg(msg,False)
            except socket.error as e:
                print("error receiving")
                print("Caught exception socket.error : %s" % e)

    def publish(self,cmdr,name,prop):
        message = cmdr + " " + name + " {:.2f}%"
        message = message.format(prop)
        if self.connected :
            self.sendMsg(message)
        self.display_msg(message,True)

    def event(self,cmdr,entry):
        #received a ProspectedAsteroid event
        #check for materials
        for mat in entry['Materials']:
            if mat['Name'] == "LowTemperatureDiamond" and self.track_LTD == 1 :
                if mat['Proportion'] > float(self.ltd_threshold):
                    self.publish(cmdr,mat['Name_Localised'],mat['Proportion'])
                elif self.miss == 1 :
                    self.display_msg("Asteroid below threshold",True)
            elif mat['Name'] == "Painite" and self.track_Painite == 1 :
                if mat['Proportion'] > float(self.painite_threshold):
                    self.publish(cmdr,mat['Name_Localised'],mat['Proportion'])
                elif self.miss == 1 :
                    self.display_msg("Asteroid below threshold",True)
            elif self.miss == 1 :
                self.display_msg("Wrong Asteroid",True)
