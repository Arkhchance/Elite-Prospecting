class Node(object):

	def sendMsg(self , sock , message):
		sock.sendall(message.encode())

	def recvMsg(self, sock , delimeter):
		data = sock.recv(4096)
		return data.decode()
