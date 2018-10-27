## This is a simple program to run thrusters/servo motors using the python maestro module
import sys
from libraries.maestro import * ## this needs to be fixed
import control
import time

## This is to prevent the thruster from running for ridiculous time inputs
maxTime = 10;
minTime = 2;
## Input through system command, the channel of the thruster
## this input must be between and including 1-8
tChan = int(sys.argv[1]);
## Receives speed from and including -1.0 - 1.0
## this will change when we start using the joystick
tSpeed = int(sys.argv[2]);
## Receives input for how long the thruster should run in seconds.
## an input of 3, will run the thruster for 3 seconds.
## this will be changed when joystick is used
## Use common sense when inputing time
tTime = int(sys.argv[3]);
## set run time to minTime if user input is not between and including maxTime and minTime
tTime = tTime if (tTime <= maxTime and tTime >= minTime) else minTime;
## 8 ports are available for thrusters.
PORTS = [0,1,2,3,4,5,6,7,8];

## Inits the maestro controller from the library.
servo = maestro.Controller();
## Initialize the control module with maestro channel and thruster port
dt = control.Thruster(servo, PORTS[tChan]);
## run the thruster for tTime
dt._fly(tSpeed);
time.sleep(tTime);
## stop the thruster after tTime.
dt._stop();
