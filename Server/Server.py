import socket
from socket import AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, SHUT_RDWR
import ssl
from base64 import b64encode
from base64 import b64decode
import json
import PasswordMan as ps

#Create and define variables
listen_addr = '127.0.0.1'
listen_port = 2706
server_cert = 'SSLserver.crt'
server_key = 'SSLserver.key'
client_certs = 'SSLclient.crt'

#Context
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain(certfile=server_cert, keyfile=server_key)
context.load_verify_locations(cafile=client_certs)

#Bind to the socket
bindsocket = socket.socket()
bindsocket.bind((listen_addr, listen_port))
bindsocket.listen(5)

while True:
    print("Waiting for client")
    newsocket, fromaddr = bindsocket.accept()
    print("Client connected: {}:{}".format(fromaddr[0], fromaddr[1])"\n")
    conn = context.wrap_socket(newsocket, server_side=True)
    print("SSL established. Peer: {}".format(conn.getpeercert())"\n")

    try:
        # Receive the data in small chunks
        while True:
            action = bytes.decode(conn.recv(4096), 'utf-8')

            if(action):



            else:
                break
