"""Video - Toggle LED."""
import sys
import serial

# Serial setup
ser = serial.Serial('/dev/ttyACM2', 115200)

# Set LED brightness
ledduty = int(sys.argv[1])

send = ("{ LED:" + str(ledduty) + " }")
if (ser.isOpen() is False):
    ser.open()
ser.write(send.encode("utf-8"))

# Close serial connection
ser.close()
