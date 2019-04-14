#/usr/bin/python3

import socket
import os

PORT = 8998
HOST = "0.0.0.0"

def generate_key(secret_key_size = 10):
    return int.from_bytes(os.urandom(secret_key_size),"big")
    
def steve():
    # generate secret key
    secret_key = generate_key()

    # initialize common key and state
    common_key = None
    state = None
    
    # create socket
    sck = socket.socket()
    sck.bind((HOST,PORT))
    sck.listen(5)
    
    while 1:
        c,_ = sck.accept()
        
        # get common key
        common_key = int(c.recv(1000))
        
        # state 1
        state = common_key + secret_key
        
        # send state 1
        c.send(bytes(str(state),'utf-8'))
        
        # receive their state 1
        state1 = int(c.recv(100))

        # close socket
        c.close()
        #sck.close()
        
        # final state
        state = state1 + secret_key

        print("Secret Key:",secret_key)
        print("Shared Key:",state)
        #return state

def do_diffie_hellman(steve,steves_port=PORT,secret_key_size = 10):
    # generate secret key
    secret_key = generate_key()

    # generate common key
    common_key = generate_key()
    
    # generate socket
    sck = socket.socket()
    sck.connect((steve,steves_port))

    # send common key
    sck.send(bytes(str(common_key),'utf-8'))

    # state 1
    state = common_key + secret_key

    # get state 1
    state1 = int(sck.recv(100))
    
    # send state 1
    sck.send(bytes(str(state),'utf-8'))

    # final state
    state = state1 + secret_key
    
    print("Secret Key:",secret_key)
    print("Shared Key:",state)
    
    #return ""