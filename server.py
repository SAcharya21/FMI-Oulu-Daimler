import socket
import time

# GETTING SERVER INFORMATION
HOST = socket.gethostbyname(socket.gethostname())
PORT = 6000
ADDR = (HOST, PORT)

# STARTING SERVER
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen(5)

# RECEIVE ADDRESS FROM CLIENTS AND PRINTING IT
# SENDING BYTEARRAY TO CLIENT
# LENGTH OF BYTE_ARRAY IS 5
# IF A PISTON IS ACTIVATED - STOP THE LINE AFTER DELAY
print(f"Server {ADDR}")
while True:
    # ACCEPT CONNECTION
    client, address = server.accept()
    print(f"Connected with {address}")
    while True:
        byte_array = []
        byte = input("Enter a byte: ")
        for i in range(len(byte)):
            byte_array.append(int(byte[i]))
        print(byte_array)

        client.send(bytes(byte_array))

        if byte_array[2:3] == [1]:
            print('[VALVE 1] Opened')
            time.sleep(1)
            byte_array[2:3] = [0]
            client.send(bytes(byte_array))
            print('[VALVE 1] Closed')
        if byte_array[3:4] == [1]:
            print('[VALVE 2] Opened')
            time.sleep(1)
            byte_array[3:4] = [0]
            client.send(bytes(byte_array))
            print('[VALVE 2] Closed')
        if byte_array[4:5] == [1]:
            print('[VALVE 3] Opened')
            time.sleep(1)
            byte_array[4:5] = [0]
            client.send(bytes(byte_array))
            print('[VALVE 3] Closed')
