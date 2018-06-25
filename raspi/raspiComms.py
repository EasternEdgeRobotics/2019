import socket
import sys

#TODO: Change to Hungarian notation
#TODO: Add sending thread
    #s.sendto(input().encode('utf-8'), (ipSend, portSend))

#TODO: Change to raspi ip for deploy
    #ipSend = 'localhost'
    #portSend = 5001
#TODO: Change to getting proper ip of computer
ipHost = 'localhost'
portHost = 5000

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    #TODO: Change to writing to an error file
    print("Failed To Create Socket")
    sys.exit()
#TODO: Check for exceptions for communication operations
s.bind((ipHost, portHost))
data, addr = s.recvfrom(1024)
data = data.decode("utf-8")
nextSpace = data.find(" ")
#TODO: Handle last item better. Follow last item with a space right now
if nextSpace == -1:
    file = data
else:
    file = data[0:nextSpace]
while nextSpace != -1:
    lastSpace = nextSpace
    nextSpace = data.find(" ", nextSpace + 1)
exec(open(file).read())
