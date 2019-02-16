"""Program to run the thruster and servo motors using the python maestro module."""
import sys
sys.path.append('libraries')
import maestro
import control

# Inputs through system command
# The channel of the thruster from and including 0 to 9
tChan = int(sys.argv[1])
# Speed from and including -1.0 to 1.0
tSpeed = float(sys.argv[2])
flag.set()
# 8 ports are available for thrusters and 2 for servos
PORTS = [0, 1, 2, 3, 7, 15, 16, 17, 8, 11]
# Inits the maestro controller from the library.
servo = maestro.Controller()
# Initialize the control module with maestro channel and thruster port
dt = control.Thruster(servo, int(PORTS[tChan]))
# Run the thruster
dt.Fly(tSpeed)
