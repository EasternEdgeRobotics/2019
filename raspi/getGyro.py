

#!/usr/bin/python
import serial
import syslog
import time

flag.set()

#The following line is for serial over GPIO
port = '/dev/ttyACM0'


ard = serial.Serial(port,115200,timeout=5)
time.sleep(2) # wait for Arduino



while 1:
#    ard.write(str.encode("Gyro_x"))
#    time.sleep(6)
    msg = (ard.read(ard.inWaiting()))
#    msg = ard.readline()
    msg = str(msg)
#    find_y = msg.find('GyroY')
#    find_x = msg.find('GyroX')
#    find_z = msg.find('GyroZ')
#    gyro_z = msg[find_z:find_z+10]
#    gyro_z = gyro_z.split(':')
#    gyro_x = msg[find_x:find_x+10]
#    gyro_x = gyro_x.split(':')
#    gyro_y = msg[find_y:find_y+10]
#    gyro_y = gyro_y.split(':')

#    gyro_y = float(gyro_y[1])
#    gyro_x = (gyro_x[1])
#    gyro_z = float(gyro_z[1])
    send.put(msg)
#    send.put("y " + str(gyro_y))
#    send.put("z " + str(gyro_z))
#    print(msg)
    time.sleep(.80); ## .75

raise Exception(str(msg))
