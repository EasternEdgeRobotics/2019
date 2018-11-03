"""
This is control software for flow.

This program should receive joystick
values for topsides through /raspiComms.py/ and user system commands to
run the thrusters.

- this program will receive 2 values /direction and responsiveness/
- change response constant in /control.py/ to receive value from sys
- set thruster values based on /direction/ input
"""

import sys
sys.path.append('libraries')
import maestro
import control


servo = maestro.Controller()

"""
Receive rov actions through system commands
These values are set on topsides using the sliders and
joystick coordinates. The coordinates of the joysticks are
vectored on topsides.
"""
tDirect = (sys.argv[1]).lower()
tPos = int(sys.argv[2])
# tResponse = int(sys.argv[3]);
# Thruster.RESPONSE = tResponse;

"""
These are constant thruster values
F is +max_speed, B is -max_speed and C is stop/center
These values may be too high for the rov. They must be tested.
"""
F = 1.0
B = -1.0
C = 0.0

"""
Create port objects for the control module
Initialize 6 thruster ports using the maestro channedl and port #
"""
PORT_0 = control.Thruster(servo, 0)
PORT_1 = control.Thruster(servo, 1)
PORT_2 = control.Thruster(servo, 2)
PORT_3 = control.Thruster(servo, 3)
PORT_4 = control.Thruster(servo, 4)
PORT_5 = control.Thruster(servo, 5)


def moveThruster(p0, p1, p2, p3, p4, p5):
    """Function to set run the thrusters based on the value given."""
    PORT_0.Fly(p0)
    PORT_1.Fly(p1)
    PORT_2.Fly(p2)
    PORT_3.Fly(p3)
    PORT_4.Fly(p4)
    PORT_5.Fly(p5)


"""
Based on the direction given by the javascript file,
set the thrusters to the appropriate value.
"""
if(tDirect == "surge" and tPos == 1):
    moveThruster(F, B, B, F, C, C)
elif(tDirect == "surge" and tPos == -1):
    moveThruster(B, F, F, B, C, C)
elif(tDirect == "sway" and tPos == 1):
    moveThruster(F, F, B, B, C, C)
elif(tDirect == "sway" and tPos == -1):
    moveThruster(B, B, F, F, C, C)
elif(tDirect == "heave" and tPos == 1):
    moveThruster(C, C, C, C, F, F)
elif(tDirect == "heave" and tPos == -1):
    moveThruster(C, C, C, C, B, B)
elif(tDirect == "pitch" and tPos == 1):
    moveThruster(C, C, C, C, F, B)
elif(tDirect == "pitch" and tPos == -1):
    moveThruster(C, C, C, C, B, F)
elif(tDirect == "yaw" and tPos == 1):
    moveThruster(F, B, F, B, C, C)
elif(tDirect == "yaw" and tPos == -1):
    moveThruster(B, F, B, F, C, C)
else:
    moveThruster(C, C, C, C, C, C)
