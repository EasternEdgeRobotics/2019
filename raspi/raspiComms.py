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
    #TODO: Change to message sent back to gui
    print("Failed To Create Socket")
    sys.exit()

s.bind((ipHost, portHost))
while True:
    data, addr = s.recvfrom(1024)
    data = data.decode("utf-8")
    if data == "exit":
        break
    nextSpace = data.find(".py") + 3
    file = data[0:nextSpace]
    lastSpace = nextSpace + 1
    nextSpace = data.find(" ", lastSpace)
    while nextSpace != -1:
        sys.argv.append(data[lastSpace:nextSpace])
        lastSpace = nextSpace + 1
        nextSpace = data.find(" ", lastSpace)
    sys.argv.append(data[lastSpace:])
    try:
        exec(open(file).read())
    except ValueError as e:
        #TODO: Change to message sent back to gui
        print(e)
    except FileNotFoundError as e:
        #TODO: Change to message sent back to gui
        print(e)
    del sys.argv[1:]
