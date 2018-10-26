## This is a simple program to run thrusters/servo motors using the python maestro module
import sys
from libraries.maestro import *
import control
import time

## This will automatically throw an error if one occurs.
try:
    ## Input through system command, the channel of the thruster
    ## this input must be between and including 1-8
    tChan = sys.argv[1];
    ## Receives speed from and including -1.0 - 1.0
    ## this will change when we start using the joystick
    tSpeed = sys.argv[2];
    ## Receives input for how long the thruster should run in seconds.
    ## an input of 3, will run the thruster for 3 seconds.
    ## this will be changed when joystick is used
    ## Use common senser when inputing time
    tTime = sys.argv[3];
    ## 8 ports are available for thrusters.
    PORTS = [None,1,2,3,4,5,6,7,8];

    ## Inits the maestro controller from the library.
    servo = maestro.Controller();
    ## Initialize the control module with maestro channel and thruster port
    dt = control.Thruster(servo, PORTS[tChan]);
    ## run the thruster for tTime
    dt._fly(tSpeed);
    time.sleep(tTime);
    ## stop the thruster after tTime.
    dt._stop();
