""" Setup constants for control loop
-Import control module from library
-Import pid module from library
-take imputs as system arguments
-set target
-Calculate error
-set integral
-calculate derivative and update error
"""
import math
import time
import sys
sys.path.append('raspi/libraries')
import maestro
import pidh

cDepth = int(sys.argv[1]); ## Get current depth
targetDepth = int(sys.argv[2]); ## Get the target depth value

depth = pid(); ## make a depth object of the pid class
## initialize depth pid constants
def depth_PID_init():
    depth.kP = 0.0
    depth.kI = 0.0
    depth.kD = 0.0

def set_depth_target(target):
    depth.target = target

def depth_PID():
    depth_PID_init();
    intError = 0;
    depth.error = depth.target - abs(cDepth);
    if(abs(depth.error) < intError):
        depth.integral += 1;
    else:
        depth.integral = 0;

    depth.integral = 0 if depth.error == 0;
    depth.derivative = depth.error - depth.last_error;
    depth.last_error = depth.error;
