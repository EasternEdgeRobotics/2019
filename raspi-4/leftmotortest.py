"""Video - Left Motor."""
import sys
import serial
import time
import RaspiGlobals

# Serial setup
#ser = serial.Serial('/dev/ttyACM0', 115200)

# Initialize claw position
'''direction = flag['claw']'''

# Loop checking for updates with a small delay
'''while True:
    if direction == flag['claw']:
        time.sleep(0.05)
        continue

    direction = flag['claw']'''

# Set motor direction
#direction = sys.argv[1]

def moveLeftMotor(ser, direction):
    # Set motor speed (timings are based on this value)
    duty = 80
    # Open or close motor
    if (direction == "open"):
        # Move motor
        send = ("{ motor:3" + ", " + "1" + ", " + str(duty) + " }")
        if ser.isOpen() is False:
            ser.open()
        ser.write(send.encode("utf-8"))
        ser.flush()

        time.sleep(0.5)

        # Stop motor
        send = ("{ motor:3" + ", " + "1" + ", " + "0" + " }")
        ser.write(send.encode("utf-8"))
        ser.flush()

    elif (direction == "close"):
        # Move motor
        send = ("{ motor:3" + ", " + "0" + ", " + str(duty) + " }")
        if ser.isOpen() is False:
            ser.open()
        ser.write(send.encode("utf-8"))
        ser.flush()

        time.sleep(0.5)

        # Stop motor
        send = ("{ motor:3" + ", " + "1" + ", " + "0" + " }")
        ser.write(send.encode("utf-8"))
        ser.flush()

    elif (direction == "stop"):
        # Stop motor
        send = ("{ motor:3" + ", " + "1" + ", " + "0" + " }")
        if ser.isOpen() is False:
            ser.open()
        ser.write(send.encode("utf-8"))
        ser.flush()

    else:
        print("Not a valid argument")

# Update the JSON
#RaspiGlobals.editJSON("claw-pos", direction)
