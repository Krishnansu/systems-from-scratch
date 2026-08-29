import socket


class HTTPRequest:

    def __init__(
        self,
        method,
        path,
        version,
        headers,
        body
    ):
        self.method = method
        self.path = path
        self.version = version
        self.headers = headers
        self.body = body


def parse_request(buffer):

    header_end = buffer.find(
        b"\r\n\r\n"
    )

    if header_end == -1:
        return None

    header_bytes = buffer[:header_end]

    remaining = buffer[
        header_end + 4:
    ]

    lines = header_bytes.split(
        b"\r\n"
    )

    request_line = lines[0].decode()

    method, path, version = (
        request_line.split(" ")
    )

    headers = {}

    for line in lines[1:]:

        name, value = line.split(
            b":",
            1
        )

        name = (
            name
            .decode()
            .strip()
            .lower()
        )

        value = (
            value
            .decode()
            .strip()
        )

        headers[name] = value

    content_length = int(
        headers.get(
            "content-length",
            0
        )
    )

    if len(remaining) < content_length:
        return None

    body = remaining[
        :content_length
    ]

    return HTTPRequest(
        method,
        path,
        version,
        headers,
        body
    )


def create_response(request):

    if (
        request.method == "GET"
        and request.path == "/hello"
    ):

        body = "Hello, World!"

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

server.bind(
    ("localhost", 8080)
)

server.listen()

print(
    "Server listening on "
    "http://localhost:8080"
)


while True:

    connection, address = (
        server.accept()
    )

    print(
        "Client connected:",
        address
    )

    buffer = b""

    while True:

        data = connection.recv(
            4096
        )

        if not data:
            break

        buffer += data

        request = parse_request(
            buffer
        )

        if request is None:
            continue

        print(
            "Method:",
            request.method
        )

        print(
            "Path:",
            request.path
        )

        print(
            "Headers:",
            request.headers
        )

        print(
            "Body:",
            request.body
        )

        response = create_response(
            request
        )

        connection.send(
            response.encode()
        )

        break

    connection.close()