"""Communicate from server to client side."""
import socket
import sys
import threading
import queue
from RaspiGlobals import GLOBALS

send = queue.Queue()
t = []

# TODO: Change to topsides ip
ipSend = GLOBALS['ipSend']
portSend = GLOBALS['portSend']
ipHost = GLOBALS['ipHost']
portHost = GLOBALS['portHost'] + 4

#try opening a socket for communication
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    # TODO: Change to message sent back to gui
    print("Failed To Create Socket")
    sys.exit()
# bind the ip and port of the raspi to the socket and loop coms
s.bind((ipHost, portHost))

#this function sends data to topsides
def sendData():
    global s, send
    sendData = send.get()
    while sendData != "exit":
        s.sendto(sendData.encode('utf-8'), (GLOBALS['ipSend'], GLOBALS['portSend']))
        print("sent response: " + sendData + " to " + str(ipSend) + " " + str(portSend))
        sendData = send.get()
    s.sendto(sendData.encode('utf-8'), (GLOBALS['ipSend'], GLOBALS['portSend']))
    print("sent response: " + sendData + " to " + str(ipSend) + " " + str(portSend))

#this function receives data from topsides
def receiveData():
    global t
    while True:
        # receive the data from topsides
        data, addr = s.recvfrom(1024)
        data = data.decode("utf-8")
        if data == "exit":
            send.put("exit")
            break
        elif data == "register":
            ipSend = addr[0]
            print(ipSend)
            s.sendto(("sensorPi").encode('utf-8'), (ipSend, GLOBALS['portSend']))
            continue
        print(data)
        # identify the file name and arguements
        nextSpace = data.find(".py") + 3
        file = data[0:nextSpace]
        lastSpace = nextSpace + 1
        nextSpace = data.find(" ", lastSpace)
        while nextSpace != -1:
            sys.argv.append(data[lastSpace:nextSpace])
            lastSpace = nextSpace + 1
            nextSpace = data.find(" ", lastSpace)
        sys.argv.append(data[lastSpace:])

        # Setup threading for receiving data
        flag = threading.Event()
        t.append(threading.Thread(target=executeData, args=(file, flag,)))
        print(t)
        t[len(t) - 1].start()
        flag.wait()
        del sys.argv[1:]
        t = [i for i in t if i.isAlive()]

def executeData(file, flag):
    try:
        exec(open(file).read(), {"send":send, "flag":flag})
    except Exception as e:
        send.put(str(e))
        flag.set()

# Setup threading for receiving data
t.append(threading.Thread(target=sendData))

if __name__ == "__main__":
    t[0].start()
    receiveData()