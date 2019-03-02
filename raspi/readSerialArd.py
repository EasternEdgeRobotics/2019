
#!/usr/bin/python
import serial
import syslog
import time
import json
flag.set()

#The following line is for serial over GPIO
port = '/dev/ttyACM0'


ard = serial.Serial(port,115200,timeout=5)
time.sleep(2) # wait for Arduino

while True:
  # Serial read section
  send.put(str(ard.readline())) # send vals to topsides

raise Exception('err');
