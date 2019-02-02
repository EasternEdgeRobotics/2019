

#!/usr/bin/python
import serial
import syslog
import time

#The following line is for serial over GPIO
port = "/dev/cu.usbmodem14201" ##'/dev/ttyACMO'


ard = serial.Serial(port,115200,timeout=5)
time.sleep(2) # wait for Arduino

i = 0

while i < 5:
    msg = str(ard.read(ard.inWaiting()))
    #print(msg,"\n\n")

    find_y = msg.find('Accely')
    find_x = msg.find('Accelx')
    accelx = msg[find_x:find_x+12]
    accelx = accelx.split(':')
    accely = msg[find_y:find_y+12]
    accely = accely.split(':')
    try:
        accelx = float(accelx[1])
        accely = float(accely[1])
        #print(accelx, accely);
        ## send accel values
    except:
        continue

    i = i + 1
    time.sleep(.075); ## .75

print("End");
