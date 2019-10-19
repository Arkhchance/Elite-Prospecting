#!/usr/bin/python
import sys
import Tkinter as tk
import myNotebook as nb
from config import config
from Prospecting import Prospecting

this = sys.modules[__name__]
prospecting = None

def plugin_prefs(parent,cmdr,is_beta):
    PADX = 10
    BUTTONX = 12	# indent Checkbuttons and Radiobuttons
    PADY = 2		# close spacing
    row = 1
    frame = nb.Frame(parent)
    frame.columnconfigure(1, weight=1)


    this.ltd_p = tk.IntVar(value=config.getint("track_LTD") and 1)
    this.painite_p = tk.IntVar(value=config.getint("track_Painite") and 1)
    this.new_win = tk.IntVar(value=config.getint("use_new_window") and 1)
    this.win_trans = tk.IntVar(value=config.getint("win_trans") and 1)
    this.miss = tk.IntVar(value=config.getint("miss") and 1)

    this.ip_label = nb.Label(frame,text="Server IP")
    this.ip_label.grid(row=row, padx=PADX, sticky=tk.W)
    this.server_ip = nb.Entry(frame)
    this.server_ip.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

    row += 1
    this.port_label = nb.Label(frame,text="Server Port")
    this.port_label.grid(row=row, padx=PADX, sticky=tk.W)
    this.server_port = nb.Entry(frame)
    this.server_port.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

    row += 1
    this.font_size_label = nb.Label(frame,text="font size")
    this.font_size_label.grid(row=row, padx=PADX, sticky=tk.W)
    this.font_size = nb.Entry(frame)
    this.font_size.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

    row += 1
    nb.Checkbutton(frame, text='Display result on new window (restart edmc)', variable=this.new_win).grid(row=row, column=0, padx=PADX, pady=PADY, sticky=tk.EW)
    row += 1
    nb.Checkbutton(frame, text='Make the window transparent (windows only)', variable=this.win_trans).grid(row=row, column=0, padx=PADX, pady=PADY, sticky=tk.EW)
    row += 1
    nb.Checkbutton(frame, text='Display message if asteroid target doesn\'t meet requirement', variable=this.miss).grid(row=row, column=0, padx=PADX, pady=PADY, sticky=tk.EW)

    row += 1
    this.my_color_label = nb.Label(frame,text="My Color : ")
    this.my_color_label.grid(row=row, padx=PADX, sticky=tk.W)
    this.my_color = nb.Entry(frame)
    this.my_color.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)
    row += 1
    this.color_label = nb.Label(frame,text="Others Color : ")
    this.color_label.grid(row=row, padx=PADX, sticky=tk.W)
    this.color = nb.Entry(frame)
    this.color.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

    row += 1
    nb.Checkbutton(frame, text='Search for LTD greater than', variable=this.ltd_p).grid(row=row, column=0, padx=PADX, pady=PADY, sticky=tk.EW)
    this.ltd_threshold = nb.Entry(frame)
    this.ltd_threshold.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

    row += 1
    nb.Checkbutton(frame, text='Search for Painite greater than', variable=this.painite_p).grid(row=row, column=0, padx=PADX, pady=PADY, sticky=tk.EW)
    this.painite_threshold = nb.Entry(frame)
    this.painite_threshold.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

    load_value()
    return frame

def load_value():
    ltd_t = config.get("LTD_t") or 18
    port = config.get("server_port") or 44988
    ip = config.get("server_ip") or "127.0.0.1"
    painite_t = config.get("Painite_t") or 25
    font_size = config.get("font_size") or 14
    my_color = config.get("my_color") or "Red"
    color = config.get("color") or "Yellow"

    this.ltd_threshold.insert(0,ltd_t)
    this.server_port.insert(0,port)
    this.server_ip.insert(0,ip)
    this.painite_threshold.insert(0,painite_t)
    this.font_size.insert(0,font_size)
    this.my_color.insert(0,my_color)
    this.color.insert(0,color)

def prefs_changed(cmdr,is_beta) :
    global prospecting

    config.set("track_LTD", this.ltd_p.get())
    config.set("track_Painite", this.painite_p.get())
    config.set("LTD_t", this.ltd_threshold.get())
    config.set("Painite_t",this.painite_threshold.get())
    config.set("server_ip",this.server_ip.get())
    config.set("server_port",this.server_port.get())
    config.set("font_size",this.font_size.get())
    config.set("use_new_window",this.new_win.get())
    config.set("win_trans",this.win_trans.get())
    config.set("miss",this.miss.get())
    config.set("my_color",this.my_color.get())
    config.set("color",this.color.get())

    prospecting.load_config(True)

def plugin_start3(plugin_dir):
    return plugin_start(plugin_dir)

def plugin_app(parent):
    global prospecting
    prospecting.init_gui(parent)

def plugin_start(plugin_dir):
    global prospecting
    prospecting = Prospecting()

def journal_entry(cmdr,is_beta,system,station,entry,state):
    global prospecting
    if entry['event'] == "ProspectedAsteroid":
        prospecting.event(cmdr,entry)

def plugin_stop():
    global prospecting
    prospecting.stop()
