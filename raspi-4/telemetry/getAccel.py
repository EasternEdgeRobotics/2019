

#!/usr/bin/python
import serial
import syslog
import time

#The following line is for serial over GPIO
port = "/dev/cu.usbmodem14201" ##'/dev/ttyACMO'


ard = serial.Serial(port,115200,timeout=5)
time.sleep(2) # wait for Arduino

msg = str(ard.read(ard.inWaiting()))


find_y = msg.find('Accely')
find_x = msg.find('Accelx')
find_z = msg.find('Accelz')
accelx = msg[find_x:find_x+12]
accelx = accelx.split(':')
accely = msg[find_y:find_y+12]
accely = accely.split(':')
accelz = msg[find_z:find_z+12]
accelz = accelz.split(':')

try:
    accelx = float(accelx[1])
    accely = float(accely[1])
    accelz = float(accelz[1])
    print("X: ",accelx, "Y: ",accely, "Z: ", accelz)
    ## send accel values
except:
    print("")

def get():
    return {"x": accelx, "y": accely, "z": accelz}

print("End")
