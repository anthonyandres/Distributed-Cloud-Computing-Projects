import logging

import grpc
import lab3_pb2
import lab3_pb2_grpc
from concurrent import futures

import requests
import pika
import time
import random
# import string
# import hashlib

i = 0


def removeFormat(body):
    s = str(body).replace('\'', '')
    ss = s.replace('b', '')
    return ss


def on_message_received(ch, method, properties, body):
    #print("\nTETSETSETSETSETSE\n")
    global i
    receivedBody = removeFormat(body)
    if i == 0:
        print(f"\ndefused mine serial number: {receivedBody}")
        i = 1
    elif i == 1:
        print(f"defused mine PIN: {receivedBody}")
        i = 2
    elif i == 2:
        print(f"defused mine ID: {receivedBody}")
        i = 0


class getMapServicer(lab3_pb2_grpc.groundControlServicer):
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
        return lab3_pb2.MapArray(ma=mapString, columns=columns, rows=rows)


class getCommandServicer(lab3_pb2_grpc.CommandServiceServicer):
    def getCommand(self, request, context):
        botID = request.bi
        response = requests.get("https://coe892.reev.dev/lab1/rover/%d" % botID)
        data1 = response.json()['data']["moves"]
        return lab3_pb2.moveString(ms=data1)


class getMineSerialServicer(lab3_pb2_grpc.MineSerialServiceServicer):
    def getMineSerial(self, request, context):
        # randomSerialNumber = random.randint(0, 999999)
        # f"{randomSerialNumber:06d}"
        # file_name = 'mineSerialTemplate.txt'
        # with open(file_name, 'w') as f:
        #     f.write(f"{randomSerialNumber}\n")
        mineSerialNumber = 111111  # default value for serial number
        f = open("mineSerialTemplate.txt", "r")
        coordinates = request.mr
        testString = f.read()
        #print(testString)
        justChars = []
        for ch in testString:
            justChars.append(''.join(ch))
        #print(justChars)
        stringx = "".join(justChars)
        #print(stringx)
        newList = stringx.split("\n")
        #print(newList)
        for word in newList:
            if word.startswith(coordinates):
                mineSerialNumber = int(word[3:len(word)])
        return lab3_pb2.mineSerialInt(msi=mineSerialNumber)


class incomingNotiServicer(lab3_pb2_grpc.DefusedMineNotificationServiceServicer):
    def incomingNoti(self, request, context):
        print("-----------------------------")
        connectionParameters = pika.ConnectionParameters('localhost')
        connection = pika.BlockingConnection(connectionParameters)
        channel = connection.channel()
        global i
        channel.queue_declare(queue='defusedMines')
        for method_frame, properties, body in channel.consume(queue='defusedMines', auto_ack=True):
            receivedBody = removeFormat(body)
            if i == 0:
                print(f"\ndefused mine serial number: {receivedBody}")
                i = 1
            elif i == 1:
                print(f"defused mine PIN: {receivedBody}")
                i = 2
            elif i == 2:
                print(f"defused mine ID: {receivedBody}")
                i = 0
                #requeued_messages=channel.cancel()
                #print('Requeued %i messages' % requeued_messages)
                break

            # if method_frame.deliver_tag == 3:
            #     break

        channel.stop_consuming()
        channel.close()
        connection.close()


        #channel.queue_declare(queue='defusedMines')
        #channel.basic_consume(queue='defusedMines', auto_ack=True, on_message_callback=on_message_received)
        print("\n")
        #channel.consume(queue='defusedMines', inactivity_timeout=3)
        #channel.start_consuming()

        # channel.close()
        # connection.close()
        return lab3_pb2.confirmation(c="received")

# class notifyServerServicer(lab3_pb2_grpc.commandCompletionNotificationServicer):
#     def notifyServer(self, request, context):
#         notice = request.n
#         botID = request.bi
#         if notice == True:
#             confirmation = "bot %d succeeded!" % botID
#         else:
#             confirmation = "bot %d failed..." % botID
#         return lab2_pb2.confirmation(c=confirmation)
#
#
# class shareMinePinServicer(lab2_pb2_grpc.incomingMinePinServicer):
#     def shareMinePin(self, request, context):
#         minePin = request.mp
#         botID = request.bi
#         confirmation = "mine pin: " + minePin + ", from bot " + str(botID)
#         return lab2_pb2.confirmation(c=confirmation)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lab3_pb2_grpc.add_CommandServiceServicer_to_server(getCommandServicer(), server)
    # lab3_pb2_grpc.add_commandCompletionNotificationServicer_to_server(notifyServerServicer(), server)
    lab3_pb2_grpc.add_MineSerialServiceServicer_to_server(getMineSerialServicer(), server)
    lab3_pb2_grpc.add_groundControlServicer_to_server(getMapServicer(), server)
    # lab3_pb2_grpc.add_incomingMinePinServicer_to_server(shareMinePinServicer(), server)
    lab3_pb2_grpc.add_DefusedMineNotificationServiceServicer_to_server(incomingNotiServicer(), server)

    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
