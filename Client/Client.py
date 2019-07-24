import socket
import sys
import time
import getpass
import ssl
from Crypto.Cipher import AES
from Crypto import Random


#Function to send Data to the server.
def sendData(action, *args):
    #variables
    host_port = 2706
    server_sni_hostname = 'example.com'
    server_cert = 'SSLserver.crt'
    client_cert = 'SSLclient.crt'
    client_key = 'SSLclient.key'
    #hostname = '192.168.0.99'
    hostname = 'localhost'
    result = 'none'

    #context
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
    context.load_cert_chain(certfile=client_cert, keyfile=client_key)

    # Connect the socket to the port where the server is listening
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn = context.wrap_socket(s, server_side=False, server_hostname=server_sni_hostname)
    conn.connect((hostname, host_port))

    try:

        # Send Action
        conn.sendall(bytes(action, 'utf-8'))
        time.sleep(.0002)

        #Send the arguments
        for arg in args:
            conn.sendall(bytes(arg, 'utf-8'))
            time.sleep(.0002)

        # Look for the response
        amount_received = 0
        amount_expected = len(result)
        while(amount_received < amount_expected):
            result = conn.recv(64)
            amount_received += len(result)
            return(bytes.decode(result, 'utf-8'))

    finally:
        conn.close()

#Creates a function to check for numbers  in strings
def num_there(s):
    return any(i.isdigit() for i in s)



#Actual Client
#Displays starting Message and gets the users choice
choice = input("Welcome! Type 'new' to create a user or 'login' to login: ")

#If their choice was to create a new user
if(choice.lower() == 'new'):

    #Enters used username loop
    x = 1
    while(x == 1):

        #Enters good password loop
        y = 1
        while(y == 1):

            #Sets action
            action = 'write'

            #Gets username and pass
            username = input('Username: ')
            password = getpass.getpass(prompt='Password: ', stream=None)
            email = input('Email: ')

            #Checks to see if it's a good password
            if(password == password.lower()):
                    print('Please include a capital letter')

            if(num_there(password) == False):
                print('Please include a number')

            if(password != password.lower() and num_there(password) == True):
                y = 0

        #Send auth packet and saves result
        result = sendData(action, username, password, email)
        password = "****"

        #Checks to see if account was created successfuly
        if(result == 'success'):
            print('Created new account!')
            x = 0
            choice = "login"
        if(result == 'used'):
            print('Username already in use, try another')
            y = 1

#If their choice was to Login
if(choice.lower() == 'login'):

    #starts auth loop
    x = 1
    while(x == 1):

        #Set action and get username and password
        action = 'read'
        username = input('Username: ')
        password = getpass.getpass(prompt='Password: ', stream=None)

        #sends auth packet
        result = (sendData(action, username, password))
        password = "****"

        #Check to see if auth succeeded
        if(result):
            if(result == 'fail'):
                print('Failed to login. Check username and password')
            else:
                print('Key: ' + str(result))
                x = 0

#Initiallizes Command loop
z = 1
while(z == 1):
    command = input('==> ')

    if(command.lower() == 'key'):
        print(result)
    if(command.lower() == 'help'):
        print('\nHelp: Prints this message\nExit: Exits the program\n')
    if(command.lower() == 'exit'):
        z = 0
    if(command.lower() == 'update email'):
        print(sendData('UpdateEmail', result, input('New Email: ')))
