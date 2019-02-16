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
sys.path.append('../libraries')
import maestro
from pidh import pid

depth = pid(); ## make a depth object of the pid class-----------
## initialize depth pid constants

cDepth = float(sys.argv[1]); ## Get current depth
depth.target = float(sys.argv[2]); ## Get the target depth value


"""  PID constants must be tuned to prevent oscillation"""
def depth_PID_init():
    depth.kP = 0.375 ## don't go any higher than 0.009 otherwise, oscillation increases by about 10%
    depth.kI = 0.0354
    depth.kD = 0.025

depth.error = depth.target - abs(cDepth);

def depth_PID():

    depth_PID_init() ## initialize PID constants
    intError = 0.5 ## increases or decrease based on magnitude of oscillation
    depth.error = (depth.target - abs(cDepth)) ## Keep current depth at an absolute value

    ## increase integral if the error does not zero out as power decreases
    if(abs(depth.error) < intError):
        depth.integral += .01
    else:
        depth.integral = 0

    depth.integral = 0 if depth.error == 0 else depth.integral
    depth.derivative = depth.error - depth.last_error
    depth.last_error = depth.error

    power = (depth.error*depth.kP)+(depth.integral*depth.kI)+(depth.derivative*depth.kD)
    print('\nPower = ',power, "Error = ",depth.error, "Current D = ",cDepth, "target = ", depth.target)

## run depth_PID when module is called
if __name__ == '__main__':
    count = 0
    while(depth.error > 0 and count < 150):
        depth_PID()
        cDepth += .02;
        count+=2
