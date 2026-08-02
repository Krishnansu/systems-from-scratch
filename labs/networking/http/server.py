import socket


def create_response(method, path):

    if method == "GET" and path == "/hello":
        body = "Hello, World!"

        return (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            f"Content-Length: {len(body)}\r\n"
            "\r\n"
            f"{body}"
        )

    if method == "GET" and path == "/about":
        body = "This is my server."

        return (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            f"Content-Length: {len(body)}\r\n"
            "\r\n"
            f"{body}"
        )

    body = "404 Not Found"

    return (
        "HTTP/1.1 404 Not Found\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {len(body)}\r\n"
        "\r\n"
        f"{body}"
    )


server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind(("localhost", 8080))
server.listen()

print("Server listening on http://localhost:8080")


while True:

    connection, address = server.accept()

    print("Client connected:", address)

    data = connection.recv(4096)

    request = data.decode()

    request_line = request.split("\r\n")[0]

    method, path, version = request_line.split(" ")

    print(
        f"{method} {path} {version}"
    )

    response = create_response(
        method,
        path
    )

    connection.send(
        response.encode()
    )

    connection.close()