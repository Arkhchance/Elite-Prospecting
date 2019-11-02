#!/usr/bin/python
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk 
import socket
import sys
import time
import threading
import hashlib
import json
from config import config
from Sound import Sound


class Prospecting():
    def __init__(self):
        self.connected = False
        self.gui_init = False
        self.msg_send = False
        self.run = True
        self.parent = None
        self.total_msg = 0
        self.messages = []
        self.hashlist = []
        self.colors = []
        self.total_msg_display = 6
        self.mw_status = [None] * self.total_msg_display
        self.status = [None] * self.total_msg_display
        self.buffer = 1024
        self.ore = 0
        self.qty_cargo = 0
        self.sound = Sound()
        self.load_config()

    def load_config(self, change = False):
        self.ip = config.get("EP_server_ip") or "37.59.36.212"
        self.port = int(config.get("EP_server_port") or 44988)
        self.session = config.get("EP_session") or "default"

        self.track_LTD = config.getint("EP_track_LTD")
        self.track_Painite = config.getint("EP_track_Painite")
        self.new_win = config.getint("EP_use_new_window")
        self.win_trans = config.getint("EP_win_trans")
        self.miss = config.getint("EP_miss")
        self.track_cargo = config.getint("EP_track_cargo")
        self.play_sound = config.getint("EP_sound")

        self.ltd_threshold = int(config.get("EP_LTD_t") or 18)
        self.painite_threshold = int(config.get("EP_Painite_t") or 25)
        self.font_size = int(config.get("EP_font_size") or 14)

        self.my_color = config.get("EP_my_color") or "Red"
        self.color = config.get("EP_color") or "Blue"

        self.pos_x = config.getint("EP_pos_x") or 200
        self.pos_y = config.getint("EP_pos_y") or 200

        # sanity check
        if len(self.session) > 15:
            self.session = "default"

        if change :
            self.change_session()
            self.update_gui()
            self.refresh_display()
            self.refresh_cargo()

    def init_gui(self, parent):
        self.parent = parent
        self.frame = tk.Frame(self.parent, borderwidth=2)
        self.frame.grid(sticky=tk.NSEW, columnspan=2)

        row = 0
        self.connection = tk.Button(self.frame, text="Connect to server", command=self.connect)
        self.connection.grid(row=row, padx=0)
        row += 1
        self.mw_cargo = tk.Label(self.frame, text="Cargo : ")
        self.mw_cargo.config(font=("Courier", int(self.font_size)))
        self.mw_cargo.grid(row=row, pady=5, sticky=tk.W)


        for i in range(self.total_msg_display):
            self.mw_status[i] = tk.Label(self.frame, text="", foreground="yellow")
            self.mw_status[i].config(font=("Courier", int(self.font_size)))
            row += 1
            self.mw_status[i].grid(row=row, pady=5, sticky=tk.W)

        self.win_x = tk.Scale(self.frame, from_=1, to=6000, orient=tk.HORIZONTAL, label="x position",command=self.update_new_win)
        self.win_x.grid(row=row+3, columnspan=2)
        self.win_x.set(self.pos_x)
        row += 1
        self.win_y = tk.Scale(self.frame, from_=1, to=3000, orient=tk.HORIZONTAL, label="y position",command=self.update_new_win)
        self.win_y.grid(row=row+6, columnspan=2)
        self.win_y.set(self.pos_y)

        self.update_gui()
        self.gui_init = True
        return self.frame

    def update_gui(self):
        try:
            self.window.destroy()
        except AttributeError as e:
            print("window not created ", e)
        if self.new_win == 1:
            self.win_x.grid()
            self.win_y.grid()
            self.mw_cargo.grid_remove()
            for i in range(self.total_msg_display):
                self.mw_status[i].grid_remove()

            self.window = tk.Toplevel()
            if sys.platform == 'win32' and self.win_trans == 1:
                self.window.attributes("-transparentcolor", 'black')
            self.window.wm_attributes("-topmost", True)
            self.window.overrideredirect(True)
            self.window.configure(background='black')

            self.cargo = tk.Label(self.window, text="Cargo : ")
            self.cargo.config(font=("Courier", int(self.font_size)),background='black')
            self.cargo.pack(side="top", fill="both", expand=True, padx=10, pady=10)

            for i in range(self.total_msg_display):
                self.status[i] = tk.Label(self.window)
                self.status[i].config(font=("Courier", int(self.font_size)),background='black')
                self.status[i].pack(side="top", fill="both", expand=True, padx=10, pady=10)
                if i == 0:
                    self.status[i]['text'] = "Waiting..."
            self.window.wm_geometry('+' + str(self.pos_x) + '+' + str(self.pos_y))
            if self.track_cargo == 0:
                self.cargo.pack_forget()
        else:
            if self.track_cargo == 1:
                self.mw_cargo.grid()
            else:
                self.mw_cargo.grid_remove()
            self.win_x.grid_remove()
            self.win_y.grid_remove()
            for i in range(self.total_msg_display):
                self.mw_status[i].grid()

    def update_new_win(self,val):
        self.pos_x = self.win_x.get()
        self.pos_y = self.win_y.get()
        if self.new_win == 1:
            self.window.wm_geometry('+' + str(self.win_x.get()) + '+' + str(self.win_y.get()))

    def display_msg(self, msg, mine=True):
        if mine:
            color = "mine"
        else:
            color = "other"

        self.colors.append(color)
        self.messages.append(msg)
        self.total_msg += 1

        if self.total_msg > self.total_msg_display:
            self.messages.pop(0)
            self.colors.pop(0)
            self.total_msg -= 1

        self.refresh_display()

    def refresh_display(self):
        for i in range(len(self.messages)):
            if self.colors[i] == "mine":
                color = self.my_color
            else:
                color = self.color
            if self.new_win == 1:
                self.status[i].config(foreground=color)
                self.status[i]['text'] = self.messages[i]
            else:
                self.mw_status[i].config(foreground=color)
                self.mw_status[i]['text'] = self.messages[i]

    def process_msg(self, json_data):
        msg_hash = json_data['hash']
        msg = json_data['cmdr']
        if msg_hash in self.hashlist:
            # duplicate !
            if self.miss == 1 :
                msg += " duplicate"
                self.display_msg(msg, False)
            return # stop here
        else:
            self.hashlist.append(msg_hash)

        if self.play_sound == 1 :
            self.sound.play()

        msg += " " + json_data['data']
        self.display_msg(msg, False)

    def refresh_cargo(self):
        if self.track_cargo == 1:
            if self.new_win == 1 :
                self.cargo['text'] = "Cargo : " + str(self.qty_cargo) + " Ore : " + str(self.ore)
            else:
                self.mw_cargo['text'] = "Cargo : " + str(self.qty_cargo) + " Ore : " + str(self.ore)

    def sendMsg(self, message):
        try:
            self.sock.sendall(message.encode())
        except socket.error as e:
            print("error sending")
            print("Caught exception socket.error : %s" % e)
            self.stop()
        self.msg_send = True

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connection["text"] = "Connecting..."
            print("connecting to ", self.ip)
            self.sock.connect((self.ip, int(self.port)))

        except socket.error as e:
            print("Caught exception socket.error : %s" % e)
            print("Error connecting")
            self.connection["text"] = "Error connecting check configuration"
            return

        con_succes = {
            "act" : "connexion",
            "data" : "Player join"
        }
        self.connected = True
        self.change_session()
        time.sleep(1)
        self.sendMsg(json.dumps(con_succes).encode())
        threading.Thread(target=self.recvs).start()
        threading.Thread(target=self.heart_beat).start()
        self.connection["text"] = "Connected"
        time.sleep(2)
        self.connection.grid_remove()

    def change_session(self):
        to_send = {
            "act" : "session",
            "data" : self.session
        }
        if self.connected:
            self.sendMsg(json.dumps(to_send))

    def stop(self):
        config.set("EP_pos_x", self.pos_x)
        config.set("EP_pos_y", self.pos_y)
        if not self.connected:
            return
        self.run = False
        self.connected = False
        quit_msg = {"act": "quit"}
        self.sendMsg(json.dumps(quit_msg))
        time.sleep(1)
        try:
            self.sock.close()
        except socket.error as e:
            print("socket.error : %s" % e)

        self.connection.grid()

    def recvMsg(self):
        data = self.sock.recv(self.buffer)
        return data.decode()

    def heart_beat(self):
        hb = {
            "act" : "keep_alive",
            "data" : "ping"
        }
        hb = json.dumps(hb)
        while self.run:
            if not self.msg_send:
                self.sendMsg(hb)
            else :
                self.msg_send = False
            time.sleep(10)

    def recvs(self):
        while self.run:
            try:
                msg = self.recvMsg()
            except socket.error as e:
                print("error receiving")
                print("Caught exception socket.error : %s" % e)
                self.stop()

            try:
                decoded = json.loads(msg)
                if decoded['act'] == "quit":
                    self.stop()
                    break
                elif decoded['act'] == "event":
                    self.process_msg(decoded)
                elif decoded['act'] == "connexion":
                    self.display_msg(decoded['data'], True)
            except ValueError as e:
                print("Bad formating ",e)

    def publish(self, cmdr, name, prop, hash, duplicate):
        data = name + " {:.2f}%"
        data = data.format(prop)
        message = {
            "act" : "event",
            "cmdr" : cmdr,
            "data" : data,
            "hash" : hash
        }

        if self.connected:
            self.sendMsg(json.dumps(message))
        if not duplicate:
            if self.play_sound == 1:
                self.sound.play()
            to_display = cmdr + " " + name + " {:.2f}%"
            self.display_msg(to_display.format(prop), True)

    def cargo_event(self, entry):
        if "Count" in entry:
            self.qty_cargo = entry['Count']
            if self.qty_cargo == 0:
                self.ore = 0
                self.hashlist.clear()
            self.refresh_cargo()

    def refined_event(self):
        self.ore += 1
        self.refresh_cargo()

    def event(self, cmdr, entry):
        # received a ProspectedAsteroid event
        empty = True
        below_t = False
        duplicate = False

        mat_hash = hashlib.md5(json.dumps(entry["Materials"]).encode()).hexdigest()

        if mat_hash in self.hashlist:
            duplicate = True
        else:
            self.hashlist.append(mat_hash)

        # check for materials
        for mat in entry['Materials']:
            if mat['Name'] == "LowTemperatureDiamond" and self.track_LTD == 1 :
                if mat['Proportion'] > float(self.ltd_threshold):
                    self.publish(cmdr, mat['Name_Localised'], mat['Proportion'], mat_hash, duplicate)
                else:
                    below_t = True
                empty = False
            elif mat['Name'] == "Painite" and self.track_Painite == 1 :
                if mat['Proportion'] > float(self.painite_threshold):
                    self.publish(cmdr, "Painite", mat['Proportion'], mat_hash, duplicate)
                else:
                    below_t = True
                empty = False

        if self.miss == 1:
            if duplicate:
                self.display_msg("Asteroid already prospected", True)
                return
            if empty and not below_t:
                self.display_msg("Asteroid without materials", True)
            if below_t:
                self.display_msg("Threshold not met", True)
