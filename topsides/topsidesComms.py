import socket
import sys

#TODO: Change to Hungarian notation
#TODO: Add receiving thread
    #s.bind((ipHost, portHost))
    #data, addr = s.recvfrom(1024)
    #data = data.decode("utf-8")

#TODO: Change to raspi ip for deploy
ipSend = 'localhost'
portSend = 5000
#TODO: Change to getting proper ip of computer
    #ipHost = 'localhost'
    #portHost = 5001

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    #TODO: Change to ouput on gui
    print("Failed To Create Socket")
    sys.exit()
while True:
    data = input()
    s.sendto(data.encode('utf-8'), (ipSend, portSend))
    if data == "exit":
        break
