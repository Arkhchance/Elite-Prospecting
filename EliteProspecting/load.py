#!/usr/bin/python
import socket , sys , signal
from threading import Thread

#comodity
lookFor = "LowTemperatureDiamond"

#threshold
threshold = 18

#serveraddr
ip = "arkhchance.ovh"

#port
port = 44988
client = None

def plugin_start(plugin_dir):
    global client
    client = Client(ip, port, name)
    client.start()



def journal_entry(cmdr,is_beta,system,station,entry,state):
    global client
    if entry['event'] == "ProspectedAsteroid":
        print(cmdr)
        for i in entry['Materials']:
            if i['Name'] == lookFor and i['Proportion'] > threshold :
                msg = i['Name_Localised'] + " {:.2f}  %"
                client.sends(cmdr,msg.format(i['Proportion']))

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

	def sends(self,cmdr, msg):
		message = cmdr + " : " + msg
		self.sendMsg(message)

	def recvs(self):
		while True:
			msg = self.recvMsg()
			print(msg)
