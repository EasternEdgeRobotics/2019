import maestro
import sys



## This will automatically throw an error if one occurs.

## Inits the maestro controller from the library.
servo = maestro.Controller()


## get accel, target and speed values from system command
accel = int(sys.argv[1])
target = int(sys.argv[2])
speed = int(sys.argv[3])

## There are only 2 thruster ports at the momemt.
## Additional ports can be easily appended
port = [1,1]

## Set accel, target and speed for port 0
servo.setAccel(port[0], accel)
servo.setTarget(port[0], target)
servo.setSpeed(port[0], speed)


print(servo.getPosition(0))
