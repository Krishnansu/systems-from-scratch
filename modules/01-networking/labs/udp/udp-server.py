import socket

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

server.bind(("127.0.0.1", 9000))

print("UDP server listening...")

while True:
    data, address = server.recvfrom(1024)

    print(
        f"Received {data.decode()} "
        f"from {address}"
    )

    server.sendto(
        b"ACK",
        address
    )