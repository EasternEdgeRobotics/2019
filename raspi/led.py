"""Toggle LED."""
import sys
import serial

# Serial port
ser = serial.Serial('TTYACM2', 115200)

# Set LED
ledduty = int(sys.argv[1])
send = ("{ LED:" + str(ledduty) + " }")
print(send)
(ser.isOpen() is False):
    ser.open()
ser.write(send.encode("utf-8"))
ser.close()
