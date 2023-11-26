import socket

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    client.connect(("192.168.189.1",5555))
    while True:
        print(client.recv(2048).decode())

except Exception as e:
    print(e)
