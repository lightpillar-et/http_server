import socket 

host = "127.0.0.1"
port = 8080

# create socket (IPv4 + TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind socket to address
server_socket.bind((host, port))

# start listening
server_socket.listen()
print(f"Server is listening on {host}:{port}")

# accept connectino
connection_socket, client_address = server_socket.accept()
print(f"Connection accepted from {client_address}")

# receive raw data (bytes)
raw_request_data = connection_socket.recv(1024)

print("----- RAW HTTP REQUEST -----")
print(raw_request_data)

# decode bytes → string
request = raw_request_data.decode()

# build HTTP response
response = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/plain\r\n"
    "Content-Length: 5\r\n"
    "\r\n"
    "Hello"
)

# send response (string → bytes)
connection_socket.send(response.encode())

# close sockets
connection_socket.close()
server_socket.close()