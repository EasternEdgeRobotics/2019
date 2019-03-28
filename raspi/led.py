"""Toggle LED."""
import sys
import serial

# Serial port
ser = serial.Serial('/dev/ttyACM2', 115200)

# Set LED
ledduty = int(sys.argv[1])

flag.set()

send = ("{ LED:" + str(ledduty) + " }")
(ser.isOpen() is False):
    ser.open()
ser.write(send.encode("utf-8"))
ser.close()
