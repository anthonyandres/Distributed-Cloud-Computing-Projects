import random
import string
import hashlib
import sys

import requests
mainurl="https://lab4-fast-api.azurewebsites.net"
mainalturl="http://20.175.174.71"
#botID = int(sys.argv[1])

def switch(inputa):
    if inputa == "create":
        commands = input("input commands: ")
        ID = input("input ID: ")
        url = mainurl+"/rovers?id={ID}&commands={commands}".format(ID=ID, commands=commands)
        print(requests.post(url).json())

    elif inputa == "all rovers":
        print("list of all rovers:")
        print(requests.get(mainurl+"/rovers").json())

    elif inputa == "rover":
        ID = input("input ID: ")
        print("info on rover with ID: ")
        print(requests.get(mainurl+"/rovers/{ID}".format(ID=ID)).json())

    elif inputa == "delete":
        ID = input("input ID: ")
        print(requests.delete(mainurl+"/rovers/{ID}".format(ID=ID)).json())
        print("deleted rover with ID: ")

    elif inputa == "dispatch":
        ID = input("input ID: ")
        commands = requests.get(mainurl+"/rovers/{ID}".format(ID=ID)).json()['rover commands']
        map = requests.get(mainurl+"/map").json()['map']
        columns = requests.get(mainurl + "/map").json()['columns']
        rows = requests.get(mainurl + "/map").json()['rows']

        justChars = []
        for ch in map:
            justChars.append(''.join(ch))
        # print(justChars)

        mapMetaInfo = []
        mapMetaInfo.append(justChars[0])
        mapMetaInfo.append(justChars[1])
        # print(mapMetaInfo)

        justMap = map.replace(str(columns), '')
        justMap = justMap.replace(str(rows), '')
        # print("justmap: " + justMap)

        charArray = []
        for i in range(0, len(justMap), columns):
            charArray.append(justMap[i:i + columns])
        # print(charArray)

        split = []
        finalMap = []
        finalMap.append(mapMetaInfo)
        for lista in charArray:
            for ch in lista:
                split.append(''.join(ch))
            array = split.copy()
            finalMap.append(array)
            split.clear()

        print("FINAL MAP LIST:")
        print(finalMap)





        new_path = bot_process(commands, finalMap)
        list_of_bot_path = []
        list_of_bot_path.append(new_path)
        i = 0
        j = 0
        finalposition=""
        print(new_path)
        for path in new_path:
            j = 0
            for ch in path:
                if ch == 'x':
                    finalposition = str(j)+str(i)
                    print("FINAL POSITION")
                    print(finalposition)
                j+=1

            i+=1

        i = 1
        for path in list_of_bot_path:
            write_map_array(path, "bot_%d_path")
            i += 1


        print("dispatched rover with ID: ")
        #print(requests.post(mainurl+f"/rovers/{id}/dispatch?final={finalposition}").json())


    elif inputa == "control":
        commands = input("input commands: ")
        ID = input("input ID: ")
        print(requests.put(mainurl+"/rovers/{ID}?commands={commands}".format(ID=ID, commands=commands)).json())

        print("sent commands to rover")

def digging(N):
    random_pin = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
    fixed_serial_num = "501052835"
    to_encode = random_pin + fixed_serial_num
    print("encoding", to_encode)
    encoded = hashlib.sha256(to_encode.encode()).hexdigest()
    return encoded


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
        if data[move] == 'M' and on_mine is True:
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
                valid_pin = False
                while valid_pin is False:
                    sha256_encoded = digging(20)
                    print(sha256_encoded)
                    #test = "000000obasorigbae0"
                    #check_test = test[:6]
                    check = sha256_encoded[:6]
                    if check == "000000":
                        print("\n\n\nmine defused!")
                        valid_pin = True
            else:
                print("no mine...")
            on_mine = False

    return bot_path


def run():
    switch(input("enter your choice:\ncreate\nall rovers\nrover\ndelete\ndispatch\n"))























    # with grpc.insecure_channel('localhost:50051') as channel1:
    #     stub1 = lab2_pb2_grpc.groundControlStub(channel1)
    #     response = stub1.getMap(lab2_pb2.filename(f="map"))
    # print("map read:\n" + response.ma + "\ncolumns: " + str(response.columns) + "\nrows: " + str(response.rows))
    # justChars = []
    # for ch in response.ma:
    #     justChars.append(''.join(ch))
    # #print(justChars)
    #
    # mapMetaInfo = []
    # mapMetaInfo.append(justChars[0])
    # mapMetaInfo.append(justChars[1])
    # #print(mapMetaInfo)
    #
    # justMap = response.ma.replace(str(response.columns), '')
    # justMap = justMap.replace(str(response.rows), '')
    # #print("justmap: " + justMap)
    #
    # charArray = []
    # for i in range(0, len(justMap), response.columns):
    #     charArray.append(justMap[i:i+response.columns])
    # #print(charArray)
    #
    # split = []
    # finalMap = []
    # finalMap.append(mapMetaInfo)
    # for lista in charArray:
    #     for ch in lista:
    #         split.append(''.join(ch))
    #     array = split.copy()
    #     finalMap.append(array)
    #     split.clear()
    #
    # print("FINAL MAP LIST:")
    # print(finalMap)
    #
    # with grpc.insecure_channel('localhost:50051') as channel2:
    #     stub2 = lab2_pb2_grpc.CommandServiceStub(channel2)
    #     response = stub2.getCommand(lab2_pb2.botID(bi=botID))
    #     botData = response.ms
    # print("commands for bot %d: " % botID)
    # print(botData)
    #
    # with grpc.insecure_channel('localhost:50051') as channel3:
    #     stub3 = lab2_pb2_grpc.MineSerialServiceStub(channel3)
    #     response = stub3.getMineSerial(lab2_pb2.mineRand(mr=botID))
    #     minePin = response.msi
    # print("random mine PIN from server: " + str(response.msi))
    #
    # with grpc.insecure_channel('localhost:50051') as channel4:
    #     stub4 = lab2_pb2_grpc.commandCompletionNotificationStub(channel4)
    #     response = stub4.notifyServer(lab2_pb2.notify(n=False, bi=botID))
    # print(response.c)
    #
    # with grpc.insecure_channel('localhost:50051') as channel5:
    #     stub5 = lab2_pb2_grpc.incomingMinePinStub(channel5)
    #     response = stub5.shareMinePin(lab2_pb2.minePin(mp=str(minePin), bi=botID))
    # print(response.c)
    #
    # new_path = bot_process(botData, finalMap)
    # list_of_bot_path = []
    # list_of_bot_path.append(new_path)
    #
    # i = 1
    # for path in list_of_bot_path:
    #     write_map_array(path, "bot_%d_path" % botID)
    #     i += 1



if __name__ == '__main__':
    run()
