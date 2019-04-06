"""Program to run the thruster and servo motors using the python maestro module."""
import sys
sys.path.append('libraries')
import maestro
import control
from RaspiGlobals import GLOBALS

# Inputs through system command
# The channel of the thruster from and including 0 to 9
tChan = int(sys.argv[1])
# Speed from and including -1.0 to 1.0
tSpeed = float(sys.argv[2])
flag.set()
# 8 ports are available for thrusters and 2 for servos
PORTS = [GLOBALS['aft-star-vert-r'], GLOBALS['fore-port-vert-r'],
         GLOBALS['fore-star-vert-r'], GLOBALS['fore-star-horz-r'],
         GLOBALS['fore-port-horz-r'], GLOBALS['aft-port-vert-r'],
         GLOBALS['aft-port-horz-r'], GLOBALS['aft-star-horz-r'],
         GLOBALS['fore-camera-r'], GLOBALS['aft-camera-r']]
# Inits the maestro controller from the library.
servo = maestro.Controller()
# Initialize the control module with maestro channel and thruster port
dt = control.Thruster(servo, int(PORTS[tChan]))
# Run the thruster
dt.Fly(tSpeed)
