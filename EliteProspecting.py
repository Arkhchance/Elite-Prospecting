#!/usr/bin/python
import tailhead
import time
import glob
import os
import json
import socket , sys , signal
from Node import Node
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
ip = "127.0.0.1"

#port
port = 44988

class Client(Node):

	def __init__(self , host , port ,username):
		self.host = host
		self.username = username
		self.port = port
		self.sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

	def start(self):
		self.sock.connect((self.host , self.port))
		self.sendMsg(self.sock ,"hello")
		message = self.recvMsg(self.sock , '\n')
		if message.replace('\n' , '')!='~q':
			Thread(target=self.recvs , args=('\n',)).start()
		else:
			sys.exit(0)

	def sends(self,msg):
		message = self.username + " : " + msg
		self.sendMsg(self.sock , message)

	def recvs(self , delimeter):
		while True:
			msg = self.recvMsg(self.sock , delimeter)
			print(msg)

def taifFile(logfile,client):
    for line in tailhead.follow_path(logfile):
        if line is not None:
            data = json.loads(line)
            if data['event'] == "ProspectedAsteroid" :
                for i in data['Materials']:
                    if i['Name'] == lookFor and i['Proportion'] > threshold :
                        print("Found " + i['Name_Localised'] + " => " + str(i['Proportion']) + " %")
                        client.send("test")
        else:
            time.sleep(polling)

def main():
    #setup file
    #fileList = glob.glob(path + "*.log")
    #latestFile = max(fileList,key=os.path.getctime)

    client = Client(ip, port, name)
    client.start()
    msg = "test"
    while 1:
        client.sends(msg)
        time.sleep(3)
    #print(latestFile)
    #taifFile(latestFile,client)


if __name__ == "__main__":
    main()
