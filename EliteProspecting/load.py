#!/usr/bin/python
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk 
import sys
import myNotebook as nb
from config import config
from Prospecting import Prospecting

this = sys.modules[__name__]
prospecting = None


def plugin_prefs(parent, cmdr, is_beta):
    PADX = 10
    PADY = 2		# close spacing
    row = 1
    frame = nb.Frame(parent)
    frame.columnconfigure(1, weight=1)

    this.ltd_p = tk.IntVar(value=config.getint("EP_track_LTD"))
    this.painite_p = tk.IntVar(value=config.getint("EP_track_Painite"))
    this.new_win = tk.IntVar(value=config.getint("EP_use_new_window"))
    this.win_trans = tk.IntVar(value=config.getint("EP_win_trans"))
    this.miss = tk.IntVar(value=config.getint("EP_miss"))
    this.cargo = tk.IntVar(value=config.getint("EP_track_cargo"))
    this.sound = tk.IntVar(value=config.getint("EP_sound"))

    this.ip_label = nb.Label(frame, text="Server IP")
    this.ip_label.grid(row=row, padx=PADX, sticky=tk.W)
    this.server_ip = nb.Entry(frame)
    this.server_ip.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

    row += 1
    this.port_label = nb.Label(frame, text="Server Port")
    this.port_label.grid(row=row, padx=PADX, sticky=tk.W)
    this.server_port = nb.Entry(frame)
    this.server_port.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

    row += 1
    this.session_label = nb.Label(frame, text="Server room")
    this.session_label.grid(row=row, padx=PADX, sticky=tk.W)
    this.server_session = nb.Entry(frame)
    this.server_session.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

    row += 1
    this.font_size_label = nb.Label(frame, text="font size")
    this.font_size_label.grid(row=row, padx=PADX, sticky=tk.W)
    this.font_size = nb.Entry(frame)
    this.font_size.grid(row=row, column=1, padx=PADX, pady=PADY, sticky=tk.EW)

    row += 1
    nb.Checkbutton(frame, text='Play a sound when threshold is met', variable=this.sound).grid(row=row, column=0, padx=PADX, pady=PADY, sticky=tk.EW)
    row += 1
    nb.Checkbutton(frame, text='Display result on new window', variable=this.new_win).grid(row=row, column=0, padx=PADX, pady=PADY, sticky=tk.EW)
    row += 1
    nb.Checkbutton(frame, text='Make the window transparent (windows only)', variable=this.win_trans).grid(row=row, column=0, padx=PADX, pady=PADY, sticky=tk.EW)
    row += 1
    nb.Checkbutton(frame, text='Display a message if prospected asteroid doesn\'t meet requirement', variable=this.miss).grid(row=row, column=0, padx=PADX, pady=PADY, sticky=tk.EW)
    row += 1
    nb.Checkbutton(frame, text='Track your cargo', variable=this.cargo).grid(row=row, column=0, padx=PADX, pady=PADY, sticky=tk.EW)

    row += 1
    this.my_color_label = nb.Label(frame, text="My Color : ")
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
    ltd_t = config.get("EP_LTD_t") or "18"
    port = config.get("EP_server_port") or "44988"
    ip = config.get("EP_server_ip") or "37.59.36.212"
    painite_t = config.get("EP_Painite_t") or "25"
    font_size = config.get("EP_font_size") or "14"
    my_color = config.get("EP_my_color") or "Red"
    color = config.get("EP_color") or "Blue"
    session = config.get("EP_session") or "default"

    this.ltd_threshold.insert(0, ltd_t)
    this.server_port.insert(0, port)
    this.server_ip.insert(0, ip)
    this.painite_threshold.insert(0, painite_t)
    this.font_size.insert(0, font_size)
    this.my_color.insert(0, my_color)
    this.server_session.insert(0, session)
    this.color.insert(0, color)


def prefs_changed(cmdr, is_beta):
    global prospecting

    config.set("EP_track_LTD", this.ltd_p.get())
    config.set("EP_track_Painite", this.painite_p.get())
    config.set("EP_LTD_t", this.ltd_threshold.get())
    config.set("EP_Painite_t", this.painite_threshold.get())
    config.set("EP_server_ip", this.server_ip.get())
    config.set("EP_server_port", this.server_port.get())
    config.set("EP_font_size", this.font_size.get())
    config.set("EP_use_new_window", this.new_win.get())
    config.set("EP_win_trans", this.win_trans.get())
    config.set("EP_miss", this.miss.get())
    config.set("EP_my_color", this.my_color.get())
    config.set("EP_color", this.color.get())
    config.set("EP_session", this.server_session.get())
    config.set("EP_track_cargo", this.cargo.get())
    config.set("EP_sound", this.sound.get())

    prospecting.load_config(True)


def plugin_start3(plugin_dir):
    return plugin_start(plugin_dir)


def plugin_app(parent):
    global prospecting
    prospecting.init_gui(parent)


def plugin_start(plugin_dir):
    global prospecting
    prospecting = Prospecting()


def journal_entry(cmdr, is_beta, system, station, entry, state):
    global prospecting

    if entry['event'] == "ProspectedAsteroid":
        prospecting.event(cmdr,entry)
    elif entry['event'] == "Cargo":
        prospecting.cargo_event(entry)
    elif entry['event'] == "MiningRefined":
        prospecting.refined_event()

def plugin_stop():
    global prospecting
    prospecting.stop()
