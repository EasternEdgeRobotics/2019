import maestro
import sys



## Inits the maestro controller from the library.
servo = maestro.Controller();


## get accel, target and speed values from system command
accel = sys.argv[1];
target = sys.argv[2];
speed = sys.argv[3];

servo.setAccel(0, accel);
servo.setTarget(0, target);
servo.setSpeed(0, speed);

print(servo.getPosition(0));
