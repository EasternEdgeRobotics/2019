import sys
import serial

# Serial setup
ser = serial.Serial('/dev/ttyACM0', 115200)

def changeData(ser, secondary):
    send = ("{ sensorsreading:" + str(secondary) + "," + str(secondary) + " }")
    if (ser.isOpen() is False):
        ser.open()
    ser.write(send.encode("utf-8"))
    ser.flush()

if __name__ == "__main__":
    if ser.isOpen() is False:
        ser.open()
    msg = str((ser.read(ser.inWaiting())).decode("utf-8")).split(',')#[3:6]
    print(msg)
    ser.flush()
    changeData(ser, "1")
    time.sleep(0.75)
    while True:
        msg = str((ser.read(ser.inWaiting())).decode("utf-8")).split(',')#[3:6]
        print(msg)
        ser.flush()
   
