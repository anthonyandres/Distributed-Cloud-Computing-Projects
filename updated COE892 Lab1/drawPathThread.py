import requests
import json
import timeit
import threading

start = timeit.default_timer()
name_number = 1
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

def full_process(data):
    global name_number
    mapArray = read_map_file("map")
    file_name = "bot_%d_path" % name_number
    array_to_write = bot_process(data, mapArray)
    write_map_array(array_to_write, file_name)
    print("done %d! pending file write" % name_number)
    name_number += 1
    #return array_to_write

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
##########################################
# start of threading
# dictionary = {}
# for i in range(1, 11):
#     key = "t"+str(i)
#     mapArray2 = read_map_file("map")
#     value = threading.Thread()
#     dictionary[key] = value

#thread_list = []
t1 = threading.Thread(target=full_process, args=(list_of_bot_data[0],))
t1.start()
t1.join()

t2 = threading.Thread(target=full_process, args=(list_of_bot_data[1],))
t2.start()
t2.join()

t3 = threading.Thread(target=full_process, args=(list_of_bot_data[2],))
t3.start()
t3.join()

t4 = threading.Thread(target=full_process, args=(list_of_bot_data[3],))
t4.start()
t4.join()

t5 = threading.Thread(target=full_process, args=(list_of_bot_data[4],))
t5.start()
t5.join()

t6 = threading.Thread(target=full_process, args=(list_of_bot_data[5],))
t6.start()
t6.join()

t7 = threading.Thread(target=full_process, args=(list_of_bot_data[6],))
t7.start()
t7.join()

t8 = threading.Thread(target=full_process, args=(list_of_bot_data[7],))
t8.start()
t8.join()

t9 = threading.Thread(target=full_process, args=(list_of_bot_data[8],))
t9.start()
t9.join()

t10 = threading.Thread(target=full_process, args=(list_of_bot_data[9],))
t10.start()
t10.join()
# thread_list.append(t1)
# thread_list.append(t2)
# thread_list.append(t3)
# thread_list.append(t4)
# thread_list.append(t5)
# thread_list.append(t6)
# thread_list.append(t7)
# thread_list.append(t8)
# thread_list.append(t9)
# thread_list.append(t10)
#
# #to_write_list = []
# for thread in thread_list:
#     bot_path = thread.start()
#     #to_write_list.append(bot_path)
#
# for thread in thread_list:
#     thread.join()





##########################################
# the following is to be replaced by threading
# each loop of a for loop will be one thread, run in parallel
# list_of_bot_path = []
# for data in list_of_bot_data:
#     #print(bot_process(data, mapArray))
#     mapArray_redux = read_map_file("map")
#     new_path = bot_process(data, mapArray_redux)
#     list_of_bot_path.append(new_path)
#
# i = 1
# for path in list_of_bot_path:
#     write_map_array(path, "bot_%d_path" % i)
#     i += 1

print("start time:", start)
print("time elapsed since start time:", timeit.default_timer() - start)