import maestro
#import time



print("Servo Logs: ")
servo = maestro.Controller();


try:
    print("Control Starting: ");
    servo.setAccel(0, 4);
    servo.setTarget(0, 6000);
    servo.setSpeed(0, 10);
    print(servo.getPosition(0), servo.getPosition(1));

except Exception as e:
    print("Type error: " + str(e));
    servo.close();
