#!/usr/local/bin/python
__author__ = 'kalcho'

import socket

target_host = '127.0.0.1'
target_port = 80

# create a floating socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send some data
client.sendto(b'AAABBBCCC',(target_host, target_port))

# receive some data
data, addr = client.recvfrom(4096)

print(data.decode('utf-8'))
