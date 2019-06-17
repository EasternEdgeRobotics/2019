"""Video - Right Motor."""
import sys
import serial
import time
from leftmotortest import moveLeftMotor
from rightmotortest import moveRightMotor
from motorstest import moveMotors
from pebbletest import movePebbles
from ledtest import ledOn
from changeData import changeData

# Serial setup
ser = serial.Serial('/dev/ttyACM0', 115200)
if ser.isOpen() is False:
    ser.open()
time.sleep(2)
send.put("got connection")

#flag = {"leftmotor": "open", "rightmotor": "open", "pebbles": "None"}

while True:
    if ser.isOpen() is False:
        ser.open()
    msg = str((ser.readline()).decode("utf-8"))
    msg = msg[0:len(msg)-2].split(',')
    ser.flush()
    if msg[0] == "P":
        send.put("pressure " + msg[1])
        send.put("tempPS " + msg[2])
        send.put("gyro " + msg[3] + " " + msg[4] + " " + msg[5])
        send.put("accel " + msg[6] + " " + msg[7] + " " + msg[8])
        send.put("tempIMU " + msg[9])
    elif msg[0] == "S":
        send.put("temp " + msg[1])
        send.put("metal " + msg[2])
        send.put("ph " + msg[3])
        
    #print("gyro " + msg[0] + " " + msg[1] + " " + msg[2])
    if flag["leftmotor"] == "open" and flag["rightmotor"] == "open":
        moveMotors(ser, "open")
        flag["leftmotor"] = "None"
        flag["rightmotor"] = "None"
    elif flag["leftmotor"] == "close" and flag["rightmotor"] == "close":
        moveMotors(ser, "close")
        flag["leftmotor"] = "None"
        flag["rightmotor"] = "None"
    elif flag["leftmotor"] != "None":
        moveLeftMotor(ser, flag["leftmotor"])
        flag["leftmotor"] = "None"
    elif flag["rightmotor"] != "None":
        moveRightMotor(ser, flag["rightmotor"])
        flag["rightmotor"] = "None"
    if flag["pebbles"] != "None":
        movePebbles(ser, flag["pebbles"])
        flag["pebbles"] = "None"
    if flag["led"] != "None":
        ledOn(ser, flag["led"])
        flag["led"] = "None"
    if flag["sensors"] != "None":
        changeData(ser, flag["sensors"])
        flag["sensors"] = "None"
    #print(flag)
    #send.put(directions[0] + directions[1] + directions[2])
