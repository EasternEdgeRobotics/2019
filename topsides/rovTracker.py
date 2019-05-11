####################################################################################################################################################################################################

# """ ROV Tracking """
#
#
# def getAccelX():
#     decoded_bytes = received.get()
#     data = decoded_bytes.split(",")
#     return data[5]
#
# q1 = 90
# q2 = 180
# q3 = 270
#
# vt = 0
# xt = 0
# t = 0.01  # secs
# xComp = 0.0
# yComp = 0.0
#
#
# originX = 0.0
# originY = 0.0
#
# ## This must be run in a thread
# def getRovPosition():
#     # Get accel data every 10ms - same frequency as accel sensor(100 Hz)
#     while 1:
#         try:
#             # calculate accel to get magnitude of displacement
#             vt = getAccelX()*t
#             xt = abs(vt*t)
#             # calc x and y components of xt using gyro x
#             angle_x = getYawAngle();
#
#             if(angle_x >= 0 and angle_x < q1):  #(+,+)
#                 yComp += ( xt * math.degrees(math.sin(angle_x)))
#                 xComp += ( xt * math.degrees(math.cos(angle_x)))
#             elif(angle_x >= q2 and angle_x < q3): #(-,-)
#                 yComp += ( -xt * math.degrees(math.sin(angle_x)))
#                 xComp += ( -xt * math.degrees(math.cos(angle_x)))
#             elif(angle_x >= q1 and angle_x < q2): #(-,+)
#                 yComp += ( xt * math.degrees(math.cos(angle_x)))
#                 xComp += ( -xt * math.degrees(math.sin(angle_x)))
#             else:                                 #(+,-)
#                 yComp += ( -xt * math.degrees(math.cos(angle_x)))
#                 xComp += ( xt * math.degrees(math.sin(angle_x)))
#
#         except (IndexError, ValueError):
#             continue
#
#         time.sleep(t)
#         print("X: "+ xComp + " Y: "+yComp)
#
# def returnToOrigin():
#     o = abs(yComp)
#     a = abs(xComp)
#     constantSpeed = 0.3
#     # angle = arctan(o/a)
#     returnAngle = math.degrees(math.atan(o/a))
#     yaw.target = 180 - (returnAngle + 90)
#     # turn rov to return angle
#     thrusterData = {}
#     while(yaw.error > 8.0):
#         try:
#             cYaw = getYawAngle();
#         # Set thrusterData to move forward not turn
#             thrusterData = {
#                 "fore-port-horz": power,
#                 "fore-star-horz": power,
#                 "aft-port-horz": power,
#                 "aft-star-horz": -power,
#             }
#
#         for control in thrusterData:
#             val = thrusterData[control]
#             putMessage("fControl.py " + str(GLOBALS["thrusterPorts"][control]) + " " + str(val))
#
#     for control in thrusterData:
#         val = thrusterData[control]
#         putMessage("fControl.py " + str(GLOBALS["thrusterPorts"][control]) + " " + str(0.0))
#
#     # get distance to origin
#     distToPoint = math.hypot(xComp,yComp)
#
#     # move rov at "constantSpeed" to within 5cm of origin. This is to prevent collision
#     while(distToPoint > 0.5):
#
#             distToPoint = math.hypot(xComp,yComp)
#
#             for control in thrusterData:
#                 val = thrusterData[control]
#                 putMessage("fControl.py " + str(GLOBALS["thrusterPorts"][control]) + " " + str(constantSpeed))
#
#     # Stop Thrusters
#     for control in thrusterData:
#         val = thrusterData[control]
#         putMessage("fControl.py " + str(GLOBALS["thrusterPorts"][control]) + " " + str(0.0))
#

####################################################################################################################################################################################################
