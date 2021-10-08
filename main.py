import socket
import threading
import logging

# GETTING SERVER INFORMATION
HOST = socket.gethostbyname(socket.gethostname())
PORT = 6000
ADDR = (HOST, PORT)

# STARTING SERVER
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen(5)
# BYTES MEANING: [POSITION SENSOR 1, POSITION SENSOR 2, WHITE, RED, BLUE]
bytes_received = bytearray([0, 0, 0, 0, 0, 0])

print(f"[SERVER] {ADDR} Online")
client, address = server.accept()
print("[CLIENT] Connected")


# STARTS THE CONVEYOR BELT WHEN AN OBJECT TOUCHES SENSOR 1
def conv_belt():
    bytes_send = bytearray([1, 0, 0, 0, 0, 0])
    client.send(bytes(bytes_send))
    print("CONVEYOR BELT [ON]")


def color():
    white = False
    red = False
    blue = False
    if bytes_received[2:3] == bytearray([1]):
        print("[WHITE DETECTED]")
        white = True
        valve(white, red, blue)
    elif bytes_received[3:4] == bytearray([1]):
        print("[RED DETECTED]")
        red = True
        valve(white, red, blue)
    else:
        print("[BLUE DETECTED]")
        blue = True
        valve(white, red, blue)


# ACTIVATES A VALVE AFTER A DELAY TIMER IF SENSOR 2 IS TRIGGERED
def valve(white, red, blue):
    print("SENSOR 2 [TRIGGERED]")
    while white:
        bytes_received_temp = client.recv(5)
        if bytes_received_temp[1:2] == bytearray([1]):
            event.wait(0.8)
            bytes_send = bytearray([1, 0, 1, 0, 0, 0])
            client.send(bytes(bytes_send))
            print("VALVE 1 [OPEN]")
            white = False
    while red:
        bytes_received_temp = client.recv(5)
        if bytes_received_temp[1:2] == bytearray([1]):
            bytes_send = bytearray([1, 0, 0, 1, 0, 0])
            event.wait(1.8)
            client.send(bytes(bytes_send))
            print("VALVE 2 [OPEN]")
            bytes_send = bytearray([0, 0, 0, 0, 0, 0])
            event.wait(1)
            client.send(bytes(bytes_send))
            red = False
    while blue:
        bytes_received_temp = client.recv(5)
        if bytes_received_temp[1:2] == bytearray([1]):
            event.wait(3)
            bytes_send = bytearray([1, 0, 0, 0, 1, 0])
            client.send(bytes(bytes_send))
            print("VALVE 3 [OPEN]")
            blue = False


sensor1_flag = True
while True:
    event = threading.Event()
    # RECEIVING DATA REPEATEDLY FROM NX
    bytes_received = client.recv(5)

    # IF SENSOR 1 IS TRIGGERED
    while sensor1_flag:
        bytes_received = client.recv(5)
        if bytes_received[0:1] == bytearray([1]):
            sensor1_flag = False
            print("SENSOR 1 [TRIGGERED]")
            conv_belt()

    # IF ANY COLOR SENSOR WAS TRIGGERED, GO TO FUNCTION COLOR
    if (bytes_received[2:3] == bytearray([1]) or bytes_received[3:4] == bytearray([1]) or
       bytes_received[4:5] == bytearray([1])):
        print("COLOR SENSOR [TRIGGERED]")
        color()
