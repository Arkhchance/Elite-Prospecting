#!/usr/bin/python
import tailhead
import time
import glob
import os
import json
import socket , sys , signal
from threading import Thread

#username
name = "Arkhchance"

#log path
path = "/home/arkhchance/gamessd/steamapps/compatdata/359320/pfx/drive_c/users/steamuser/Saved Games/Frontier Developments/Elite Dangerous/"

#refresh rate in seconds
polling = 0.1

#comodity
lookFor = "LowTemperatureDiamond"

#threshold
threshold = 18

#serveraddr
ip = "arkhchance.ovh"

#port
port = 44988

class Client():

	def __init__(self , host , port ,username):
		self.host = host
		self.username = username
		self.port = port
		self.sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

	def start(self):
		self.sock.connect((self.host , self.port))
		self.sendMsg("hello")
		message = self.recvMsg()
		if message.replace('\n' , '')!='~q':
			Thread(target=self.recvs).start()
		else:
			sys.exit(0)

	def sendMsg(self  , message):
		self.sock.sendall(message.encode())

	def recvMsg(self):
		data = self.sock.recv(4096)
		return data.decode()

	def sends(self,msg):
		message = self.username + " : " + msg
		self.sendMsg(message)

	def recvs(self):
		while True:
			msg = self.recvMsg()
			print(msg)

def taifFile(logfile,client):
    for line in tailhead.follow_path(logfile):
        if line is not None:
            data = json.loads(line)
            if data['event'] == "ProspectedAsteroid" :
                for i in data['Materials']:
                    if i['Name'] == lookFor and i['Proportion'] > threshold :
                        msg = i['Name_Localised'] + " {:.2f}  %"
                        client.sends(msg.format(i['Proportion']))
        else:
            time.sleep(polling)

def main():
    #setup file
    fileList = glob.glob(path + "*.log")
    latestFile = max(fileList,key=os.path.getctime)

    client = Client(ip, port, name)
    client.start()
    print("reading : ",latestFile)
    taifFile(latestFile,client)


if __name__ == "__main__":
    main()
