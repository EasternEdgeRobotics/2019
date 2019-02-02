

#!/usr/bin/python
import serial
import syslog
import time

#The following line is for serial over GPIO
port = '/dev/ttyACMO'


ard = serial.Serial(port,115200,timeout=5)
time.sleep(2) # wait for Arduino

##i = 0


# Serial read section
msg = ard.read(ard.inWaiting()) # read all characters in buffer

msg = str(msg)

num = msg.find("Pressure")


pressure  = msg[num:num+14]
pressure = pressure.split(":")
pressure_value = float(pressure[1])
##print(pressure_value)

p_atm = (pressure_value*(1/1000))

depth = (p_atm*10)
print(depth, p_atm)
##i = i + 1
##time.sleep(.075); ## .75

raise Exception(str(depth));
