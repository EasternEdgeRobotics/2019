"""Video - Right Motor."""
import sys
import serial
import time
from leftmotortest import moveLeftMotor
from rightmotortest import moveRightMotor
from motorstest import moveMotors
from pebbletest import movePebbles

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
    msg = str((ser.read(ser.inWaiting())).decode("utf-8")).split(',')[3:6]
    ser.flush()
    send.put("gyro " + msg[0] + " " + msg[1] + " " + msg[2])
    #print("gyro " + msg[0] + " " + msg[1] + " " + msg[2])
    if flag["leftmotor"] == "open" and flag["rightmotor"] == "open":
        moveMotors(ser, "open")
    elif flag["leftmotor"] == "close" and flag["rightmotor"] == "close":
        moveMotors(ser, "close")
    elif flag["leftmotor"] != "None":
        moveLeftMotor(ser, flag["leftmotor"])
    elif flag["rightmotor"] != "None":
        moveRightMotor(ser, flag["rightmotor"])
    elif flag["pebbles"] != "None":
        movePebbles(ser, flag["pebbles"])
    print(flag)
    #send.put(directions[0] + directions[1] + directions[2])
    flag["leftmotor"] = "None"
    flag["rightmotor"] = "None"
    flag["pebbles"] = "None"
    time.sleep(0.75)
