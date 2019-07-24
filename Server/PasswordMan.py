from passlib.hash import argon2
import getpass
import json
import random
import string
import smtplib

#Function to create a user
def MakeUser(DesiredUser, DesiredPass, email):

    #Open up the passwords.json file
    with open("passwords.json", "r") as read_file:
        data = json.load(read_file)

    x = 0

    #Check to see username isnt used
    for users in data['user']:
        if(argon2.verify(DesiredUser, users['username']) == True):
            x = x+1

    if(x >= 1):
        return("used")

    #Hash the username and password
    userhash = argon2.hash(DesiredUser)
    passhash = argon2.hash(DesiredPass)

    #Generate unique key
    letters = string.ascii_letters
    key = ''.join(random.choice(letters) for i in range(60))

    #add creds to passwords.json
    data['user'].append({"username": userhash, "password": passhash, "email": email, "key": key})

    with open("passwords.json", 'w') as f:
        json.dump(data, f)

    return("success")

#Function to Authenticate user
def CallUser(LoginUser, LoginPass):

    #open passwords.json
    with open("passwords.json", "r") as read_file:
        data = json.load(read_file)

    #Check to see if its a user, and if its the correct password
    for users in data['user']:
        if(argon2.verify(LoginUser, users['username']) == True and argon2.verify(LoginPass, users['password']) == True):
            print(users['key'])
            return(users['key'])

    return ('fail')

def UpdateEmail(key, newEmail):
    #open passwords.json
    with open("passwords.json", "r") as read_file:
        data = json.load(read_file)

    for users in data['user']:
        if(key == users['key']):
            print('Got Key')
            users['email'] = newEmail
            with open("passwords.json", 'w') as f:
                json.dump(data, f)
            return('Success')

    return('fail')
