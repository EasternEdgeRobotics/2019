import socket
import sys
import  queue

send = queue.Queue()
received = queue.Queue()

"""
Comms start.
This function starts the comms and runs the comms loop. 
While the loop is running it will check the send queue for 
messages to send to the ROV. It can send messages back using recieved
"""
def startComms():
    #TODO: Change to raspi ip
    ipSend = '192.168.88.4'
    portSend = 8000
    ipHost = '192.168.88.42'
    portHost = 8001

    #try opening a socket for communication
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        #TODO: Change to ouput on gui
        print("Failed To Create Socket")
        sys.exit()
    except Exception as e:
        print("failed")

    #bind the ip and port of topsides to the socket and loop coms
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ipHost, portHost))
    received.put("bound")
    while True:
        #TODO: change from getting data from user to getting data from queue
        #send data to the raspi
        inputData = send.get()
        s.sendto(inputData.encode('utf-8'), (ipSend, portSend))
        if inputData == "exit":
            break
        #TODO: Change to saving to log file on error
        #receive response from raspi and log if error
        outputData, addr = s.recvfrom(1024)
        outputData = outputData.decode("utf-8")
        received.put(outputData)
        #TODO: move to a get on the server
        print(received.get())
