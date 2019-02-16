

#!/usr/bin/python
import serial
import syslog
import time

#flag.set()

#The following line is for serial over GPIO
port = "/dev/cu.usbmodem14201"


ard = serial.Serial(port,115200,timeout=5)
time.sleep(2) # wait for Arduino

i = 0

msg = str(ard.read(ard.inWaiting()))
print(msg)


# print(msg);

find_y = msg.find('GyroY')
find_x = msg.find('GyroX')
find_z = msg.find('GyroZ')
gyro_z = msg[find_z:find_z+11]
gyro_z = gyro_z.split(':')
gyro_x = msg[find_x:find_x+11]
gyro_x = gyro_x.split(':')
gyro_y = msg[find_y:find_y+11]
gyro_y = gyro_y.split(':')

try:
    gyro_y = float(gyro_y[1])
    gyro_x = float(gyro_x[1])
    gyro_z = float(gyro_z[1])
    #print(accelx, accely);
    print(gyro_x, " ",gyro_y, " ",gyro_z)
    send.put("x " + gyro_x)
    send.put("y " + gyro_y)
    send.put("z " + gyro_z)
    ## send accel values
except:
    print("")


#time.sleep(.075); ## .75

print("End");
