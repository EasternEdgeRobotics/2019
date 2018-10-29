## This is a simple program to run thrusters/servo motors using the python maestro module
import sys
from libraries.maestro import * ## this needs to be fixed
import control

## Input through system command, the channel of the thruster
## this input must be between and including 1-8
tChan = int(sys.argv[1]);
## Receives speed from and including -1.0 - 1.0
## this will change when we start using the joystick
tSpeed = float(sys.argv[2]);
## 8 ports are available for thrusters.
PORTS = [0,1,2,3,4,5,6,7,8];
## Inits the maestro controller from the library.
servo = maestro.Controller();
## Initialize the control module with maestro channel and thruster port
dt = control.Thruster(servo, PORTS[tChan]);
## run the thruster for tTime
dt.Fly(tSpeed);
