import FindLargest
import random


arrays = [[1,5,8,2,0,3,4]
         ,[8,3,5,9,2,9,4]
         ,[1,2,2,3,3,6,6,6]
         ,[]
         ,[1,1,9,9,9]
         ,[8,5,5,2]]
key = [8, 8, 1, None, None, 8]
for i in range(0, len(arrays)):
    if FindLargest.FindLargest(arrays[i]) != key[i]:
        print("Not Correct")
    else:
        print("Correct")


