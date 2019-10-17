class Node(object):

	def sendMsg(self , sock , message):
		sock.sendall(message.encode())

	def recvMsg(self, sock , delimeter):
		message = ""
		while True:
			data = sock.recv(4096).decode()
			if not data:
				break
			message+=data
			if delimeter in data:
				break
		return message
