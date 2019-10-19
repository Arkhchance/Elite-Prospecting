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
session_list = {}               #session list
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
        session_name = "default"
        session_list[session_name].append(nom)
        while run:
            msgClient = self.connexion.recv(BUFFER)

            msg = msgClient.decode()
            #if client send QUIT => terminate the conenction
            if msg == "quit" :
                quit = "quit"
                print("client exitting")
                conn_client[nom].send(quit.encode())
                break
            #change client session
            elif msg.find('session=') != -1 :
                #remove from old one

                session_list[session_name].remove(nom)
                session_name = msg.replace("session=","")
                print("client is changing to session ",session_name)
                if session_name == "quit" :
                    session_name = "default"

                if not session_name in session_list :
                    session_list[session_name] = []
                # add to new one
                session_list[session_name].append(nom)
                cleanup()
                continue 

            message = msgClient.decode()
            print("received ", message)
            # send to all client in session:
            for name in session_list[session_name]:
                if name != nom : #don't send to ourself
                    try:
                        conn_client[name].send(message.encode())
                    except socket.error as e:
                        print("error sending ",str(e))

        # close connection :
        self.connexion.close()
        del conn_client[nom]        # del from array
        session_list[session_name].remove(nom)
        print("Client disconnected")
        cleanup()
        # end function


def cleanup():
    try:
        for x in session_list:
            if x != "default":
                if len(session_list[x]) < 1 :
                    del session_list[x]
    except RuntimeError as e :
        print("error ",e)

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

    #create default session
    session_list["default"] = []

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
