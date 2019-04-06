"""Communicate from server to client side."""
import socket
import sys
import threading
import queue
from RaspiGlobals import GLOBALS

send = queue.Queue()
t = []

# Change IP addresses for a production or development environment
if ((len(sys.argv) > 1) and (sys.argv[1] == "--dev")):
    ipSend = GLOBALS['ipSend-dev']
    ipHost = GLOBALS['ipHost-dev']
else:
    ipSend = GLOBALS['ipSend']
    ipHost = GLOBALS['ipHost']

portSend = GLOBALS['portSend']
portHost = GLOBALS['portHost']

# Try opening a socket for communication
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    # TODO: Change to message sent back to gui
    print("Failed To Create Socket")
    sys.exit()
# Bind the ip and port of the raspi to the socket and loop coms
s.bind((ipHost, portHost))


def sendData():
    """Send data to topsides."""
    global s, send
    sendData = send.get()
    while sendData != "exit":
        s.sendto(sendData.encode('utf-8'), (ipSend, portSend))
        print("sent response: " + sendData + " to " + str(ipSend) + " " + str(portSend))
        sendData = send.get()
    s.sendto(sendData.encode('utf-8'), (ipSend, portSend))
    print("sent response: " + sendData + " to " + str(ipSend) + " " + str(portSend))


def receiveData():
    """Receive data from topsides."""
    global t
    while True:
        try:
            data, addr = s.recvfrom(1024)
            data = data.decode("utf-8")
        except socket.timeout as e:
            #stop the motors on a timeout
            for i in range(0, 8):
                sys.argv.append(i)
                sys.argv.append(0)
                try:
                    exec(open("fControl.py").read())
                except Exception as e:
                    response = str(e)
                    # print(response)
                del sys.argv[1:]
            continue
        #check for comms control messages
        if data == "exit":
            send.put("exit")
            break
        elif data == "register":
            ipSend = addr[0]
            print(ipSend)
            s.sendto(("thrusterPi").encode('utf-8'), (ipSend, GLOBALS['portSend']))
            continue
        print(data)
        # Identify the file name and arguments
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
        exec(open(file).read(), {"send": send, "flag": flag})
    except Exception as e:
        send.put(str(e))
        flag.set()


# Setup threading for receiving data
t.append(threading.Thread(target=sendData))

if __name__ == "__main__":
    t[0].start()
    receiveData()
