

#!/usr/bin/python
import serial
import syslog
import time

#The following line is for serial over GPIO
port = "/dev/cu.usbmodem14201" ##'/dev/ttyACMO'


ard = serial.Serial(port,115200,timeout=5)
time.sleep(2) # wait for Arduino


def get():

    msg = str(ard.read(ard.inWaiting()))
    msg = msg[4: msg.index("/r")]

    data = msg.split(",")



    """find_y = msg.find('Accely')
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
    """


    return {"pressure": float(data[0]),"temp": float(data[1]), "gyroscope": {"x": float(data[2]), "y": float(data[3]), "z": float(data[4])}, "accelerometer": {"x": float(data[5]), "y": float(data[6]), "z": float(data[7]), "IMUtemp": float(data[8])}
