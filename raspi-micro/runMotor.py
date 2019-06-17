"""Micro ROV motor testing."""
import os
import time
os.system("sudo killall pigpiod")
time.sleep(1)
os.system("sudo pigpiod")
time.sleep(1)
import pigpio

ESC = 18  # ESC GPIO pin

pi = pigpio.pi()
pi.set_servo_pulsewidth(ESC, 0)

max_value = 2000  # ESC maximum value
center_value = 1500
min_value = 1000  # ESC minimum value

print("Type the word for the function you want")
print("start OR stop")


def control():
    """Control the motor using the ESC."""
    speed = center_value
    print("Controls - a to decrease speed & d to increase speed OR q to decrease a lot of speed & e to increase a lot of speed")
    while True:
        print("speed = " + str(speed))
        pi.set_servo_pulsewidth(ESC, speed)
        inp = input()
        if inp == "q":
            speed -= 100  # Decrement the speed by a large amount
        elif inp == "e":
            speed += 100  # Increment the speed by a large amount
        elif inp == "d":
            speed += 10   # Increment the speed
        elif inp == "a":
            speed -= 10   # Decrement the speed
        elif inp == "stop":
            stop()
            break
        else:
            print("Not a valid option")


def arm():
    """Arm the ESC."""
    pi.set_servo_pulsewidth(ESC, center_value)
    control()


def stop():
    """Stop the program."""
    pi.set_servo_pulsewidth(ESC, center_value)
    pi.stop()
    os.system("sudo killall pigpiod")


# Start of the program
inp = input()
if inp == "start":
    arm()
elif inp == "stop":
    stop()
