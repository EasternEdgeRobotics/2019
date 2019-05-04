"""Video - Pebble Motor."""
import sys
import serial
import time

# Serial setup
ser = serial.Serial('/dev/ttyACM0', 115200)

# Set motor direction
direction = sys.argv[1]

# Set motor speed (timings are based on this value)
duty = 70

# Open or close motor
if (direction == "open"):
    # Move motor
    send = ("{ motor:1" + ", " + "0" + ", " + str(duty) + " }")
    if ser.isOpen() is False:
        ser.open()
    ser.write(send.encode("utf-8"))
    ser.flush()

    time.sleep(0.1)  # TODO: Figure out this time

    # Stop motor
    send = ("{ motor:1" + ", " + "1" + ", " + "0" + " }")
    ser.write(send.encode("utf-8"))
    ser.flush()

    # Close serial connection
    ser.close()
elif (direction == "close"):
    # Move motor
    send = ("{ motor:1" + ", " + "1" + ", " + str(duty) + " }")
    if ser.isOpen() is False:
        ser.open()
    ser.write(send.encode("utf-8"))
    ser.flush()

    time.sleep(0.1)  # TODO: Figure out this time

    # Stop motor
    send = ("{ motor:1" + ", " + "1" + ", " + "0" + " }")
    ser.write(send.encode("utf-8"))
    ser.flush()

    # Close serial connection
    ser.close()
else:
    print("Not a valid argument")
