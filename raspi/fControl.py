"""This is a simple program to run thrusters/servo motors using the python maestro module."""
import sys
sys.path.append('libraries')
import maestro
import control

# Input through system command, the channel of the thruster
# this input must be between and including 0-5
tChan = int(sys.argv[1])
# Receives speed from and including -1.0 - 1.0
tSpeed = float(sys.argv[2])
# 6 ports are available for thrusters.
# 2 1 3 5 0 4
# 2 1 15 17 0 16
PORTS = [2, 1, 15, 17, 0, 16]
# Inits the maestro controller from the library.
servo = maestro.Controller()
# Initialize the control module with maestro channel and thruster port
dt = control.Thruster(servo, int(PORTS[tChan]))
# Run the thruster
dt.Fly(tSpeed)
