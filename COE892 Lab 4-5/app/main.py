from fastapi import FastAPI
import requests

app = FastAPI()


############## MAP ##############
@app.get("/map")
def get_map():
    mapArray = []
    newList = []
    filename_txt = "app/map.txt"
    with open(filename_txt, "r") as f:
        for line in f.readlines():
            mapArray.append(line.replace('\n', '').split(' '))

    for innerList in mapArray:
        combined = ''.join(innerList)
        newList.append(combined)

    mapString = ''.join(newList)
    columns = int(mapArray[0][0])
    rows = int(mapArray[0][1])
    return {"map": mapString, "columns": columns, "rows": rows}


@app.put("/map")
def update_map(newmap: str):
    mapArray = []
    newList = []
    filename_txt = "app/" + newmap + ".txt"
    with open(filename_txt, "r") as f:
        for line in f.readlines():
            mapArray.append(line.replace('\n', '').split(' '))

    for innerList in mapArray:
        combined = ''.join(innerList)
        newList.append(combined)

    mapString = ''.join(newList)
    columns = int(mapArray[0][0])
    rows = int(mapArray[0][1])
    return {"map": mapString, "columns": columns, "rows": rows}


############# MINES #############
@app.get("/mines")
def get_mines():
    mineSerialNumber = 111111  # default value for serial number
    f = open("app/mineSerialTemplate.txt", "r")
    testString = f.read()
    # print(testString)
    justChars = []
    for ch in testString:
        justChars.append(''.join(ch))
    # print(justChars)
    stringx = "".join(justChars)
    # print(stringx)
    newList = stringx.split("\n")
    # print(newList)
    return {"list of mines": newList}


@app.post("/mines")
def create_mine(xCoor: str, yCoor: str, mineSerialNumber: str):
    toWrite = xCoor + yCoor + ":" + mineSerialNumber
    print(toWrite)
    f = open("app/mineSerialTemplate.txt", "a")
    f.write("\n" + toWrite)
    return{"created": xCoor+yCoor}


@app.get("mines/{id}")
def get_mine_serial(id: str):
    # default values
    mineSerialNumber = 111111
    xCoor = 0
    yCoor = 1
    f = open("app/mineSerialTemplate.txt", "r")
    testString = f.read()
    # print(testString)
    justChars = []
    for ch in testString:
        justChars.append(''.join(ch))
    # print(justChars)
    stringx = "".join(justChars)
    # print(stringx)
    newList = stringx.split("\n")
    # print(newList)
    for mine in newList:
        if mine.startswith(id):
            xCoor = id[0]
            yCoor = id[1]
            mineSerialNumber = int(mine[3:len(mine)])
    return {"mine serial number": mineSerialNumber, "x coordinate": xCoor, "y coordinate": yCoor}


@app.delete("mines/{id}")
def delete_mine(id: str):
    f = open("app/mineSerialTemplate.txt", "r")
    testString = f.read()
    f.close()
    # print(testString)
    justChars = []
    for ch in testString:
        justChars.append(''.join(ch))
    # print(justChars)
    stringx = "".join(justChars)
    # print(stringx)
    newList = stringx.split("\n")
    print(newList)
    f = open("app/mineSerialTemplate.txt", "w")
    for word in newList:
        if word.startswith(id):
            newList.remove(word)
    count = 0
    print(newList)
    for word in newList:
        if count == len(newList) - 1:
            f.write(word)
        else:
            f.write(word + "\n")
        count += 1
    f.close()
    return {"deleted": id}


@app.put("mines/{id}")
def update_mine(id: str | None = None, mineSerialNumber: str | None = None):
    #TODO: i dont really know why a mine would need to be updated but o well
    xCoor = id[0]
    yCoor = id[1]
    return {"mine serial number": mineSerialNumber, "x coordinate": xCoor, "y coordinate": yCoor}


############# ROVER #############
@app.get("/rovers")
def get_rover_list():
    mapArray = []
    newList = []
    filename_txt = "app/roverStatus.txt"
    with open(filename_txt, "r") as f:
        for line in f.readlines():
            mapArray.append(line.replace('\n', '').split(' '))

    for innerList in mapArray:
        combined = ''.join(innerList)
        newList.append(combined)

    roverString = ''.join(newList)
    return {"rover status list": newList}

@app.post("/rovers")
def create_rover(id: str, commands: str):
    f = open("app/roverStatus.txt", "a")
    f.write("\n" + id + ":NotStarted:" + "00" + commands)
    return{"created": id}

@app.get("/rovers/{id}")
def get_rover_status(id: str):
    mapArray = []
    newList = []
    filename_txt = "app/roverStatus.txt"
    status = "Not Started"  # default status value
    latestPosition = "00"
    with open(filename_txt, "r") as f:
        for line in f.readlines():
            mapArray.append(line.replace('\n', '').split(' '))
    f.close()

    for innerList in mapArray:
        combined = ''.join(innerList)
        newList.append(combined)

    response = requests.get("https://coe892.reev.dev/lab1/rover/%d" % int(id))
    data1 = response.json()['data']["moves"]
    counter = 0
    for rover in newList:
        if rover.startswith(id):
            status = rover[3:13]
            newList[counter] = rover + (" " + data1)
            latestPosition = rover[14:16]
        counter += 1

    f = open(filename_txt, "w")
    count = 0

    for word in newList:
        if count == len(newList) - 1:
            f.write(word)
        else:
            f.write(word + "\n")
        count += 1

    return {"id": id, "rover status": status, "rover commands": data1, "latest position": latestPosition}

@app.delete("/rovers/{id}")
def delete_rover(id: str):
    f = open("app/roverStatus.txt", "r")
    testString = f.read()
    f.close()
    # print(testString)
    justChars = []
    for ch in testString:
        justChars.append(''.join(ch))
    # print(justChars)
    stringx = "".join(justChars)
    # print(stringx)
    newList = stringx.split("\n")
    print(newList)
    f = open("app/roverStatus.txt", "w")
    for word in newList:
        if word.startswith(id):
            newList.remove(word)
    count = 0
    print(newList)
    for word in newList:
        if count == len(newList) - 1:
            f.write(word)
        else:
            f.write(word + "\n")
        count += 1
    f.close()
    return {"deleted": id}

@app.put("/rovers/{id}")
def send_commands(id: str, commands: str):
    mapArray = []
    newList = []
    filename_txt = "app/roverStatus.txt"
    status = "Not Started"  # default status value
    with open(filename_txt, "r") as f:
        for line in f.readlines():
            mapArray.append(line.replace('\n', '').split(' '))
    f.close()

    for innerList in mapArray:
        combined = ''.join(innerList)
        newList.append(combined)

    response = requests.get("https://coe892.reev.dev/lab1/rover/%d" % int(id))
    data1 = response.json()['data']["moves"]
    counter = 0
    for rover in newList:
        if rover.startswith(id):
            status = rover[3:13]
            newList[counter] = rover + (" " + commands)
        counter += 1

    if status == "Not Started" or status == "Finished":
        return{"ERROR": "invalid status"}

    f = open(filename_txt, "w")
    count = 0

    for word in newList:
        if count == len(newList) - 1:
            f.write(word)
        else:
            f.write(word + "\n")
        count += 1
    return{"sent commands to": id}


@app.post("/rovers/{id}/dispatch")
def dispatch_rover(id: str, final: str):
    mapArray = []
    newList = []
    filename_txt = "app/roverStatus.txt"
    status = "Not Started"  # default status value
    commands = ""
    latestPosition = "00"
    with open(filename_txt, "r") as f:
        for line in f.readlines():
            mapArray.append(line.replace('\n', '').split(' '))
    f.close()

    for innerList in mapArray:
        combined = ''.join(innerList)
        newList.append(combined)

    response = requests.get("https://coe892.reev.dev/lab1/rover/%d" % int(id))
    data1 = response.json()['data']["moves"]
    counter = 0
    for rover in newList:
        if rover.startswith(id):
            newList[rover] = id+":"+"Finished..:"+final+commands
            status = "Finished.."
            #status = rover[3:13]
            #commands = rover[16:len(rover)]
            #latestPosition = rover[14:16]
        counter += 1

    f = open(filename_txt, "w")
    count = 0

    for word in newList:
        if count == len(newList) - 1:
            f.write(word)
        else:
            f.write(word + "\n")
        count += 1
    return{"id": id, "status": status, "commands": commands, "latest Position": final}


@app.get("/")
def read_root():
    return {"Hello": "World"}
