import socket
import sys

#TODO: Change to topsides ip
ipSend = 'localhost'
portSend = 5001
ipHost = 'localhost'
portHost = 5000

#try opening a socket for communication
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    #TODO: Change to message sent back to gui
    print("Failed To Create Socket")
    sys.exit()

#bind the ip and port of the raspi to the socket and loop coms
s.bind((ipHost, portHost))
while True:
    #receive the data from topsides
    data, addr = s.recvfrom(1024)
    data = data.decode("utf-8")
    if data == "exit":
        break
    
    #identify the file name and arguements
    nextSpace = data.find(".py") + 3
    file = data[0:nextSpace]
    lastSpace = nextSpace + 1
    nextSpace = data.find(" ", lastSpace)
    while nextSpace != -1:
        sys.argv.append(data[lastSpace:nextSpace])
        lastSpace = nextSpace + 1
        nextSpace = data.find(" ", lastSpace)
    sys.argv.append(data[lastSpace:])

    #try opening and executing the file
    response = "done"
    try:
        exec(open(file).read())
    except ValueError as e:
        response = str(e)
    except FileNotFoundError as e:
        response = str(e)
    except Exception as e:
        response = str(e)
    del sys.argv[1:]
    s.sendto(response.encode('utf-8'), (ipSend, portSend))
