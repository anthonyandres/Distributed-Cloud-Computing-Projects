import logging

import grpc
import lab2_pb2
import lab2_pb2_grpc
from concurrent import futures

import requests
import random
import string
import hashlib


class getMapServicer(lab2_pb2_grpc.groundControlServicer):
    def getMap(self, request, context):
        mapArray = []
        newList = []
        filename_txt = request.f + ".txt"
        with open(filename_txt, "r") as f:
            for line in f.readlines():
                mapArray.append(line.replace('\n', '').split(' '))

        for innerList in mapArray:
            combined = ''.join(innerList)
            newList.append(combined)

        mapString = ''.join(newList)
        columns = int(mapArray[0][0])
        rows = int(mapArray[0][1])
        return lab2_pb2.MapArray(ma=mapString, columns = columns, rows=rows)


class getCommandServicer(lab2_pb2_grpc.CommandServiceServicer):
    def getCommand(self, request, context):
        botID = request.bi
        response = requests.get("https://coe892.reev.dev/lab1/rover/%d" % botID)
        data1 = response.json()['data']["moves"]
        return lab2_pb2.moveString(ms=data1)


class getMineSerialServicer(lab2_pb2_grpc.MineSerialServiceServicer):
    def getMineSerial(self, request, context):
        randomSerialNumber = random.randint(0, 999999)
        f"{randomSerialNumber:06d}"
        file_name = 'mineSerial.txt'
        with open(file_name, 'w') as f:
            f.write(f"{randomSerialNumber}\n")
        return lab2_pb2.mineSerialInt(msi=randomSerialNumber)


class notifyServerServicer(lab2_pb2_grpc.commandCompletionNotificationServicer):
    def notifyServer(self, request, context):
        notice = request.n
        botID = request.bi
        if notice == True:
            confirmation = "bot %d succeeded!" % botID
        else:
            confirmation = "bot %d failed..." % botID
        return lab2_pb2.confirmation(c=confirmation)


class shareMinePinServicer(lab2_pb2_grpc.incomingMinePinServicer):
    def shareMinePin(self, request, context):
        minePin = request.mp
        botID = request.bi
        confirmation = "mine pin: " + minePin + ", from bot " + str(botID)
        return lab2_pb2.confirmation(c=confirmation)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lab2_pb2_grpc.add_CommandServiceServicer_to_server(getCommandServicer(), server)
    lab2_pb2_grpc.add_commandCompletionNotificationServicer_to_server(notifyServerServicer(), server)
    lab2_pb2_grpc.add_MineSerialServiceServicer_to_server(getMineSerialServicer(), server)
    lab2_pb2_grpc.add_groundControlServicer_to_server(getMapServicer(), server)
    lab2_pb2_grpc.add_incomingMinePinServicer_to_server(shareMinePinServicer(), server)

    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()

