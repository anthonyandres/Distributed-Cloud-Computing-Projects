import pika


#def getIDFromPin(pin):

i = 0


def removeFormat(body):
    s = str(body).replace('\'', '')
    ss = s.replace('b', '')
    return ss


def on_message_received(ch, method, properties, body):
    global i
    receivedBody = removeFormat(body)
    if i == 0:
        print(f"defused mine serial number: {receivedBody}")
        i = 1
    elif i == 1:
        print(f"defused mine PIN: {receivedBody}")
        i = 2
    elif i == 2:
        print(f"defused mine ID: {receivedBody}")
        i = 0

    #channel.basic_publish(exchange='', routing_key='defusedMines', body=body)
    #return body


connectionParameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connectionParameters)
channel = connection.channel()

channel.queue_declare(queue='defusedMines')
message = channel.basic_consume(queue='defusedMines', auto_ack=True, on_message_callback=on_message_received)
print("\n")
channel.start_consuming()