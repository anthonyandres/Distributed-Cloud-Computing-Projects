import requests
import json
import timeit
start = timeit.default_timer()
def write_map_array(mapArray, name):
    file_name = name + '.txt'
    with open(file_name, 'w') as f:
        for line in mapArray:
            s = ' '.join(line)
            print(s)
            f.write(f"{s}\n")

def read_map_file(filename):
    mapArray = []
    filename_txt = filename + ".txt"
    with open(filename_txt, "r") as f:
        for line in f.readlines():
            mapArray.append(line.replace('\n', '').split(' '))
    return mapArray

def bot_process(data, mapArray):
    i = 0  # represents current row
    j = 0  # represents current column

    bot_path = mapArray[1:5]
    print("bot path initial", bot_path)
    # a list of lists, each element represents one row, the index within each element represents the column
    # bot_path[0][1] refers to the second index of the first element
    # bot_path = [['5', '4']]
    # print(bot_path[0][1]) = '4'

    bot_path[i][j] = '*'  # marking initial starting point of bot
    on_mine = False  # boolean used to determine if bot needs to dig or not
    #for move in range(0, 14):  # ignored row 0, since that is just auxiliary information
    for move in range(0, len(data)):
        if data[move] != 'D' and on_mine is True:
            bot_path[i][j] = 'x'  # using X to mark final resting place of bot
            print("digging did not occur, bot exploded!")
            break

        if data[move] == 'M':  # moving goes down to the next row
            if i < 3 and (bot_path[i][j] == '0' or '*'):
                print("moving...")
                i += 1
                if bot_path[i][j] == '1':
                    print("mine detected on current position!")
                    on_mine = True
                bot_path[i][j] = '*'
            else:
                print("ignored moving")

        elif data[move] == 'L':  # left moves to the right column on the same row
            if j < 4 and (bot_path[i][j] == '0' or '*'):
                print("turning left...")
                j += 1
                if bot_path[i][j] == '1':
                    print("mine detected on current position!")
                    on_mine = True
                bot_path[i][j] = '*'
            else:
                print("ignored turning left")

        elif data[move] == 'R':  # right moves to the left column on the same row
            if j > 0 and (bot_path[i][j] == '0' or '*'):
                print("turning right...")
                j -= 1
                if bot_path[i][j] == '1':
                    print("mine detected on current position!")
                    on_mine = True
                bot_path[i][j] = '*'
            else:
                print("ignored turning right")

        elif data[move] == 'D':  # TODO implement digging
            print("digging...")
            if on_mine is True:
                print("mine defused!")
            on_mine = False

    return bot_path


#[col][row]
#response1 = requests.get("https://coe892.reev.dev/lab1/rover/1")
#data = response1.json()['data']["moves"]

list_of_bot_data = []

for i in range(1, 11):
    response = requests.get("https://coe892.reev.dev/lab1/rover/%d" % i)
    data1 = response.json()['data']["moves"]
    list_of_bot_data.append(data1)
print("list of bot data", list_of_bot_data)
#print(data)
#print(len(data), "moves")

#response2 = requests.get("https://coe892.reev.dev/lab1/rover/2")
#data2 = response2.json()['data']["moves"]
#print(data2)

# writing text map onto an array
# mapArray = []
# with open("map.txt", "r") as f:
#     for line in f.readlines():
#         mapArray.append(line.replace('\n', '').split(' '))
mapArray = read_map_file("map")
print("map array", mapArray)
# with open('bot_path.txt', 'w') as f:
#     for line in mapArray:
#         s = ' '.join(line)
#         print(s)
#         f.write(f"{s}\n")

num_columns = int(mapArray[0][0])
num_rows = int(mapArray[0][1])
print("number of columns:", num_columns, "\nnumber of rows:", num_rows)


# i = 0  # represents current row
# j = 0  # represents current column
# #bot_path = [[0]*5]*4
# #bot_path = [['0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0']]
# bot_path = mapArray[1:5]
# print("bot path initial", bot_path)
# # a list of lists, each element represents one row, the index within each element represents the column
# # bot_path[0][1] refers to the second index of the first element
# # bot_path = [['5', '4']]
# # print(bot_path[0][1]) = '4'
#
# bot_path[i][j] = '*'  # marking initial starting point of bot
# on_mine = False  # boolean used to determine if bot needs to dig or not
# for move in range(0, 14):  # ignored row 0, since that is just auxiliary information
#     if data[move] != 'D' and on_mine is True:
#         bot_path[i][j] = 'x'  # using X to mark final resting place of bot
#         print("digging did not occur, bot exploded!")
#         break
#
#     if data[move] == 'M':  # moving goes down to the next row
#         if i < 3 or bot_path[i][j] == '0':
#             print("moving...")
#             i += 1
#             if bot_path[i][j] == '1':
#                 print("mine detected on current position!")
#                 on_mine = True
#             bot_path[i][j] = '*'
#         else:
#             print("ignored moving")
#
#     elif data[move] == 'L':  # left moves to the right column on the same row
#         if j < 4 or bot_path[i][j] == '0':
#             print("turning left...")
#             j += 1
#             if bot_path[i][j] == '1':
#                 print("mine detected on current position!")
#                 on_mine = True
#             bot_path[i][j] = '*'
#         else:
#             print("ignored turning left")
#
#     elif data[move] == 'R':  # right moves to the left column on the same row
#         if j > 0 or bot_path[i][j] == '0':
#             print("turning right...")
#             j -= 1
#             if bot_path[i][j] == '1':
#                 print("mine detected on current position!")
#                 on_mine = True
#             bot_path[i][j] = '*'
#         else:
#             print("ignored turning right")
#
#     elif data[move] == 'D':  # TODO implement digging
#         print("digging...")
#         on_mine = False
#'''
list_of_bot_path = []
for data in list_of_bot_data:
    #print(bot_process(data, mapArray))
    mapArray_redux = read_map_file("map")
    new_path = bot_process(data, mapArray_redux)
    list_of_bot_path.append(new_path)

i = 1
for path in list_of_bot_path:
    write_map_array(path, "bot_%d_path" % i)
    i += 1
#'''

#bot_path = bot_process(data, mapArray)
#print(bot_path)
#write_map_array(bot_path, "bot_path_1")
# for i in range(0, num_columns):  # ignored row 0, since that is just auxiliary information
#     for j in range(1, num_rows):
#         print("TODO")
print("start time:", start)
print("time elapsed since start time:", timeit.default_timer() - start)