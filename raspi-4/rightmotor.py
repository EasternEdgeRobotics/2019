"""Video - Right Motor."""
import sys
import serial
import time

# Serial setup
ser = serial.Serial('/dev/ttyACM0', 115200)

# Set motor speed (timings are based on this value)
duty = 80

#direction = threadData['claw']

#while True:
#   if direction == threadData['claw']:
#        time.sleep(0.05)
#       continue
#
#    direction = threadData['claw']

# Set motor direction
direction = sys.argv[1]

# Open or close motor
if (direction == "open"):
    # Move motor
    send = ("{ motor:4" + ", " + "1" + ", " + str(duty) + " }")
    if ser.isOpen() is False:
        ser.open()
    ser.write(send.encode("utf-8"))
    ser.flush()

    time.sleep(0.5)

    # Stop motor
    send = ("{ motor:4" + ", " + "1" + ", " + "0" + " }")
    ser.write(send.encode("utf-8"))
    ser.flush()

    # Close serial connection
    ser.close()
elif (direction == "close"):
    # Move motor
    send = ("{ motor:4" + ", " + "0" + ", " + str(duty) + " }")
    if ser.isOpen() is False:
        ser.open()
    ser.write(send.encode("utf-8"))
    ser.flush()

    time.sleep(0.5)

    # Stop motor
    send = ("{ motor:4" + ", " + "1" + ", " + "0" + " }")
    ser.write(send.encode("utf-8"))
    ser.flush()

    # Close serial connection
    ser.close()
elif (direction == "stop"):
    # Stop motor
    send = ("{ motor:4" + ", " + "1" + ", " + "0" + " }")
    if ser.isOpen() is False:
        ser.open()
    ser.write(send.encode("utf-8"))
    ser.flush()

    # Close serial connection
    ser.close()
else:
    print("Not a valid argument")
