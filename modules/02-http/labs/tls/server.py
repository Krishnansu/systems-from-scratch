import socket
import ssl

host = "example.com"
port = 443

# 1. Establish TCP connection
sock = socket.create_connection((host, port))

# 2. Create secure TLS context
context = ssl.create_default_context()

# 3. Perform TLS handshake
tls_sock = context.wrap_socket(
    sock,
    server_hostname=host
)

print("TLS version:", tls_sock.version())
print("Cipher:", tls_sock.cipher())

# 4. Inspect server certificate
print("Certificate:")
print(tls_sock.getpeercert())

# 5. Send HTTP request
request = (
    "GET / HTTP/1.1\r\n"
    "Host: example.com\r\n"
    "Connection: close\r\n"
    "\r\n"
)

tls_sock.sendall(request.encode())

# 6. Receive HTTP response
response = b""

while True:
    data = tls_sock.recv(4096)

    if not data:
        break

    response += data

print(response.decode(errors="replace"))

tls_sock.close()