#TODO research on RabbitMQ, how to subscribe to a queue and how to publish onto a channel on the RabbitMQ server
#client publishes onto a default exchange which pushes into the queue and the consumer (deminer) will consume the message
import grpc
import pika
import hashlib
import random
import string

import lab3_pb2
import lab3_pb2_grpc


def removeFormat(body):
    s = str(body).replace('\'', '')
    ss = s.replace('b', '')
    return ss


def getID(body):
    mineID = "00"
    f = open("mineSerialTemplate.txt", "r")
    testString = f.read()
    justChars = []
    for ch in testString:
        justChars.append(''.join(ch))
    stringx = "".join(justChars)
    #print(stringx)
    newList = []
    newList = stringx.split("\n")

    for mineData in newList:
        if str(body) in mineData:
            mineID = str(mineData[:2])

    return mineID


def on_message_received(ch, method, properties, body):
    receivedBody = removeFormat(body)
    print(f"Request to Defuse Mine serial number: {receivedBody}")
    serial = digging(6, receivedBody)
    print(f"mine PIN: {serial}")
    mineID = getID(receivedBody)

    channel.basic_publish(exchange='', routing_key='defusedMines', body=receivedBody)  # mine serial number
    channel.basic_publish(exchange='', routing_key='defusedMines', body=serial)  # mine PIN
    channel.basic_publish(exchange='', routing_key='defusedMines', body=mineID)  # mine ID

    with grpc.insecure_channel('localhost:50051') as channel1:
        stub1 = lab3_pb2_grpc.DefusedMineNotificationServiceStub(channel1)
        response = stub1.incomingNoti(lab3_pb2.notify(n="notification"))

    #return body


def digging(N, pin):
    #random_pin = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
    fixed_serial_num = "501052835"
    to_encode = str(pin) + fixed_serial_num
    #print("encoding", to_encode)
    encoded = hashlib.sha256(to_encode.encode()).hexdigest()
    return encoded


connectionParameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connectionParameters)
channel = connection.channel()
channel.queue_declare(queue='demineQueue')

channel.queue_declare(queue='defusedMines')


message = channel.basic_consume(queue='demineQueue', auto_ack=True, on_message_callback=on_message_received)
#channel.basic_publish(exchange='', routing_key='defusedMines', body=message)

print("started consuming")
channel.start_consuming()
# channel.stop_consuming()
# connection.close()

