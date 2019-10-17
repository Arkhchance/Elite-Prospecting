#!/usr/bin/python
import socket


def main():
    s = socket.socket()
    host = socket.gethostname()
    port = 54879
    s.bind((host, port))
    s.listen(5) 

    while True:
       c, addr = s.accept()
       print 'Got connection from', addr
       c.send('Thank you for connecting')
       c.close()




if __name__ == "__main__":
    main()
