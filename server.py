#!/usr/bin/python
import socket, sys, threading
import signal, time

#change as needed
HOST = '0.0.0.0'
PORT = 44988
BUFFER = 1024

#don't touch !
run = True
conn_client = {}                # active connection array

def receiveSignal(signalNumber, frame):
    print('Received Signal ', signalNumber)
    print("exiting..")
    run = False
    msg = "quit"
    time.sleep(2)
    for con in conn_client:
        try:
            conn_client[con].send(msg.encode())
            conn_client[con].close()
        except socket.error as e:
            print("error closing ",str(e))
    sys.exit()
    return

class ThreadClient(threading.Thread):

    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn

    def run(self):
        nom = self.getName()        # thread name
        while run:
            msgClient = self.connexion.recv(BUFFER)

            #if client send QUIT => terminate the conenction
            if msgClient.decode() == "quit" :
                print("client exitting")
                conn_client[nom].send("quit")
                break

            message = msgClient.decode()
            print("received ", message)
            # send to all client :
            for cle in conn_client:
                if cle != nom : #don't send to ourself
                    try:
                        conn_client[cle].send(message.encode())
                    except socket.error as e:
                        print("error sending ",str(e))

        # close connection :
        self.connexion.close()
        del conn_client[nom]        # del from array
        print("Client disconnected")
        # end function

def main() :

    signal.signal(signal.SIGTERM, receiveSignal)
    signal.signal(signal.SIGQUIT, receiveSignal)
    signal.signal(signal.SIGINT, receiveSignal)

    # server init
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        mySocket.bind((HOST, PORT))
    except socket.error as e:
        print("Can't bind quitting. ", str(e))
        sys.exit()

    print("Server is ready.. ")
    mySocket.listen(10)


    while run:
        connexion, adresse = mySocket.accept()
        # new thread :
        th = ThreadClient(connexion)
        th.start()

        it = th.getName()        # thread id
        conn_client[it] = connexion
        print ("Client %s connected, IP address %s, port %s." %(it, adresse[0], adresse[1]))
        # Answer to connection sucess :
        msg = "Connected"
        connexion.send(msg.encode())



if __name__ == "__main__":
    # execute only if run as a script
    main()
