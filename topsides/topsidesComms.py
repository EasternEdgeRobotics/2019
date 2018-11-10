import socket
import sys

# TODO: Change to raspi ip
ipSend = 'localhost'
portSend = 5000
ipHost = 'localhost'
portHost = 5001

# try opening a socket for communication
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    # TODO: Change to ouput on gui
    print("Failed To Create Socket")
    sys.exit()

# bind the ip and port of topsides to the socket and loop coms
s.bind((ipHost, portHost))
while True:
    # TODO: change from getting data from user to getting data from queue
    # send data to the raspi
    inputData = input()
    s.sendto(inputData.encode('utf-8'), (ipSend, portSend))
    if inputData == "exit":
        break
    # TODO: Change to saving to log file on error
    # receive response from raspi and log if error
    outputData, addr = s.recvfrom(1024)
    outputData = outputData.decode("utf-8")
    print(outputData)
