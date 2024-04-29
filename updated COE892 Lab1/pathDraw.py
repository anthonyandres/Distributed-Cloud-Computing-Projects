import requests
import json
def find_True(direction): #finds the index which the value is true
    for i in direction:
        tmp = direction.index(True, i)
    print('The index of truth is ', tmp)
    return(tmp)

response1 = requests.get("https://coe892.reev.dev/lab1/rover/1")
data1 = response1.json()['data']["moves"]
print(data1)
print(len(data1), "moves")

#response2 = requests.get("https://coe892.reev.dev/lab1/rover/2")
#data2 = response2.json()['data']["moves"]
#print(data2)

# writing text map onto an array
mapArray = []
with open("map.txt", "r") as f:
    for line in f.readlines():
        mapArray.append(line.replace('\n', '').split(' '))
print("map array:", mapArray)

num_columns = int(mapArray[0][0])
num_rows = int(mapArray[0][1])
print("number of columns:", num_columns, "\nnumber of rows:", num_rows)
# iterating through 2d map array
direction = [False, True, False, False]  # north, east, south, west
# turning CW will move the "True"  to the right
# turning CCW will move the "True to the left

for i in range(1, num_rows):  # ignored row 0, since that is just auxiliary information
    if (data1[i] == 'M'):
        print("moving")
        continue

    for j in range(num_columns):
        print("maparray[i][j]", mapArray[i][j])

#####################################################

#truth_index = find_True(direction)
#print(direction[truth_index])

'''
the bot starts in the top left corner of the map
in other words, at coordinates mapArray[0][1]
'''
