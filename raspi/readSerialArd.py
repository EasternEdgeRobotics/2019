
#!/usr/bin/python
import serial
import syslog
import time
import json
flag.set()

#The following line is for serial over GPIO
port = '/dev/ttyACM2'


ard = serial.Serial(port,115200,timeout=5)
time.sleep(2) # wait for Arduino

while True:
  # Serial read section
  ser_bytes = ard.readline()
  decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8")
  send.put(decoded_bytes)

raise Exception('err');
