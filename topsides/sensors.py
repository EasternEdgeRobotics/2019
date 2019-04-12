"""Testing code for tooling board sensor reading."""
import sys
import serial
import time
import botAPI

# Setup reading from the serial port
# (COM* for Windows and \dev\tty* for Linux)
ser = serial.Serial('COM20', 115200)

# Wait for the serial port to be opened
time.sleep(0.5)

# JSON to send to pick which sensors to read
# 0,0 => Primary sensors
# 1,0 => Temperature and PH sensors
# 0,1 => Metal detector
# 1,1 => All of the secondary sensors
send = "{ sensorsreading:" + sys.argv[1] + "," + sys.argv[2] + " }"
ser.write(send.encode("utf-8"))

# Main loop to read the sent string from the arduino
while True:
    global send
    # Decode the sent data
    # Format:
    # Primary:      P,PRESSURE,TEMPS,GYROX,GYROY,GYROZ,ACCX,ACCY,ACCZ,TEMPIMU
    # Secondary:    S,TEMP,METAL,PH
    # Note:         If a value is not set it will read "F"
    ser_bytes = ser.readline()
    decoded_bytes = ser_bytes[0:len(ser_bytes) - 2].decode("utf-8")
    # print(decoded_bytes)
    x = decoded_bytes.split(',')

    # Deal with the decoded data
    # TODO: Deal with "F" values
    if (x[0] == "P"):
        # Primary sensors
        # print("Pressure: " + x[1])
        # print("Temperature Sensor: " + x[2])
        # print("Gyro X: " + x[3])
        # print("Gyro Y: " + x[4])
        # print("Gyro Z: " + x[5])
        # print("Accelerometer X: " + x[6])
        # print("Accelerometer Y: " + x[7])
        # print("Accelerometer Z: " + x[8])
        # print("Temperature IMU: " + x[9])
        botAPI.data["pressure"] = x[1]
        botAPI.data["temperaturesensor"] = x[2]
        botAPI.data["gyroscopex"] = x[3]
        botAPI.data["gyroscopey"] = x[4]
        botAPI.data["gyroscopez"] = x[5]
        botAPI.data["accelerometerx"] = x[6]
        botAPI.data["accelerometery"] = x[7]
        botAPI.data["accelerometerz"] = x[8]
        botAPI.data["temperatureimu"] = x[9]
        botAPI.emitTelemetryData()
    elif (x[0] == "S"):
        # Secondary sensors
        # print("Temperature: " + x[1])
        # print("Metal detect: " + x[2])
        # print("PH: " + x[3])
        botAPI.data["temperatureext"] = x[1]
        botAPI.data["metaldetector"] = x[2]
        botAPI.data["ph"] = x[3]
        botAPI.emitTelemetryData()
    else:
        print("Not a valid receive")
