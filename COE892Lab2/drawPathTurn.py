import requests
import json
import timeit

start = timeit.default_timer()


def find_true(direction): #finds the index which the value is true
    tmp = direction.index(True)
    #print('The index of truth is ', tmp)
    return tmp


def write_map_array(mapArray, name):
    file_name = name + '.txt'
    with open(file_name, 'w') as f:
        for line in mapArray:
            s = ' '.join(line)
            print(s)
            f.write(f"{s}\n")
        print("\n")

def read_map_file(filename):
    mapArray = []
    filename_txt = filename + ".txt"
    with open(filename_txt, "r") as f:
        for line in f.readlines():
            mapArray.append(line.replace('\n', '').split(' '))
    return mapArray


def turn_left(direction):
    true_index = find_true(direction)
    new_direction = [False, False, False, False]
    if true_index == 0:
        new_direction[3] = True
    else:
        new_direction[true_index-1] = True
    #print("new direction", new_direction)
    return new_direction


def turn_right(direction):
    true_index = find_true(direction)
    new_direction = [False, False, False, False]
    if true_index == 3:
        new_direction[0] = True
    else:
        new_direction[true_index + 1] = True
    #print("new direction", new_direction)
    return new_direction


def bot_process(data, mapArray):
    direction = [False, False, True, False]  # north, east, south, west
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
            #if bot_path[i][j] == '0' or '*':

            if direction[0] is True: # if bot is facing north
                if i > 0 and (bot_path[i][j] == '0' or '*'):
                    print("moving north...")
                    i -= 1
                else:
                    print("ignored moving north")

            elif direction[1] is True: # if bot is facing east
                if j < 4 and (bot_path[i][j] == '0' or '*'):
                    print("moving east...")
                    j += 1
                else:
                    print("ignored moving east")

            elif direction[2] is True: # if bot is facing south
                if i < 3 and (bot_path[i][j] == '0' or '*'):
                    print("moving south...")
                    i += 1
                else:
                    print("ignored moving south")

            elif direction[3] is True: # if bot is facing west
                if j > 0 and (bot_path[i][j] == '0' or '*'):
                    print("moving west...")
                    j -= 1
                else:
                    print("ignored moving west")

            if bot_path[i][j] == '1':
                print("mine detected on current position!")
                on_mine = True
            bot_path[i][j] = '*'
            # else:
            #     print("ignored moving")

        elif data[move] == 'L':
            direction = turn_left(direction)
            nsew = find_true(direction)
            if nsew == 0:
                print("turning to face north...")
            elif nsew == 1:
                print("turning to face east...")
            elif nsew == 2:
                print("turning to face south...")
            elif nsew == 3:
                print("turning to face west...")

        elif data[move] == 'R':
            direction = turn_right(direction)
            nsew = find_true(direction)
            if nsew == 0:
                print("turning to face north...")
            elif nsew == 1:
                print("turning to face east...")
            elif nsew == 2:
                print("turning to face south...")
            elif nsew == 3:
                print("turning to face west...")

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


mapArray = read_map_file("map")
print("map array", mapArray)


num_columns = int(mapArray[0][0])
num_rows = int(mapArray[0][1])
print("number of columns:", num_columns, "\nnumber of rows:", num_rows)


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

print("start time:", start)
print("time elapsed since start time:", timeit.default_timer() - start)