#!/usr/bin/python
from king_chat import Server

#listen_ip
ip = "0.0.0.0"
#listen_port
port = 44987

def main():
    server = Server(ip, port)

    @server.on_received
    def handle(protocol, text):
        protocol.send_to_all_except_sender(text)

    server.start(wait=True)

if __name__ == "__main__":
    main()
