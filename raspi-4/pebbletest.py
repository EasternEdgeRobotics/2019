"""Video - Pebble Motor."""
import sys
import serial
import time

# Serial setup
#ser = serial.Serial('/dev/ttyACM0', 115200)

#direction = threadData['pebbles']

#while True:
#   if direction == threadData['pebbles']:
#        time.sleep(0.05)
#       continue
#
#    direction = threadData['pebbles']

# Set motor direction
#direction = sys.argv[1]

def movePebbles(ser, direction):
    # Set motor speed (timings are based on this value)
    duty = 90
    # Open or close motor
    if (direction == "open"):
        # Move motor
        send = ("{ motor:1" + ", " + "0" + ", " + str(duty) + " }")
        if ser.isOpen() is False:
            ser.open()
        ser.write(send.encode("utf-8"))
        ser.flush()

        time.sleep(0.75)

        # Stop motor
        send = ("{ motor:1" + ", " + "1" + ", " + "0" + " }")
        ser.write(send.encode("utf-8"))
        ser.flush()

    elif (direction == "close"):
        # Move motor
        send = ("{ motor:1" + ", " + "1" + ", " + str(duty) + " }")
        if ser.isOpen() is False:
            ser.open()
        ser.write(send.encode("utf-8"))
        ser.flush()

        time.sleep(0.75)

        # Stop motor
        send = ("{ motor:1" + ", " + "1" + ", " + "0" + " }")
        ser.write(send.encode("utf-8"))
        ser.flush()

    elif (direction == "stop"):
        # Stop motor
        send = ("{ motor:1" + ", " + "1" + ", " + "0" + " }")
        if ser.isOpen() is False:
            ser.open()
        ser.write(send.encode("utf-8"))
        ser.flush()

    else:
        print("Not a valid argument")
