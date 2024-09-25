import json


def sendMessageToClient(connection, message):
    message = message.tolist()

    data = json.dumps({"message": message})
    connection.sendall(data.encode())
