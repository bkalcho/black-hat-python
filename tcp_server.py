#!/usr/local/bin/python
__author__ = 'kalcho'

# Standard multi-threaded TCP server

import socket
import threading

bind_ip = '0.0.0.0'
bind_port = 9999

# create a floating socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind socket to address
server.bind((bind_ip, bind_port))

# make server listen for incomming connections
server.listen(5)

print("[*] listening on {:s}:{:d}".format(bind_ip, bind_port))

# this is our client-handling thread
def handle_client(client_socket):

    # print out what the client sends
    request = client_socket.recv(1024)

    print("[*] received: {:s}".format(request.decode('utf-8')))

    # send back a packet
    client_socket.send(b'ACK!')

    client_socket.close()


while True:
    client, addr = server.accept()

    print("[*] accepted connection from: {:s}:{:d}".format(addr[0], addr[1]))

    # spin up our client thread to handle incoming data
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
