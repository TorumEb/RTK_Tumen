import socket, pickle
import json
import numpy as np
from cameraRuspberry.cameraRPI import Camera_RPI
# Задаем адрес сервера
SERVER_ADDRESS = ('192.168.2.113', 8686)



def sendMessageToClient(connection, message):
    message = message.tolist()
    data = json.dumps({"message": message})
    connection.sendall(data.encode())
    return 0

def GetMessageFromClient(connection):
    while True:
        data = connection.recv(4096)
        #data = pickle.load(data)
        data = json.loads(data.decode())
        if data == 404:
            break
        return data
    return None

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(1)
    print('server is running, please, press ctrl+c to stop')
    connection, address = server_socket.accept()
    print("new connection from {address}".format(address=address))
    
    while True:
        data = GetMessageFromClient(connection)
        print(data)
        
        


    

if __name__ == "__main__":
    main()
