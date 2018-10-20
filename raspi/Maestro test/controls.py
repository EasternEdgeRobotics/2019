import maestro
import sys
#import time





servo = maestro.Controller();                                                   ## Inits the maestro controller from the library.

try:
    print("Control Starting: ");

    accel = sys.argv[1];                                                        ## get accel, target and speed values from system command
    target = sys.argv[2];
    speed = sys.argv[3];

    servo.setAccel(0, accel);
    servo.setTarget(0, target);
    servo.setSpeed(0, speed);

    print(servo.getPosition(0));

except Exception as e:                                                          ## Get an error and print it
    print("Type error: " + str(e));
    servo.close();                                                              
