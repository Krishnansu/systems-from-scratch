import socket

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

client.sendto(
    b"Hello UDP",
    ("127.0.0.1", 9000)
)

data, address = client.recvfrom(1024)

print("Server replied:", data.decode())