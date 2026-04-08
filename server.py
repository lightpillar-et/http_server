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
print(f"Connection accepted from {client_address} and Connection_Socket is  {connection_socket}")

# receive raw data (bytes)
raw_request_data = connection_socket.recv(1024)

print("----- RAW HTTP REQUEST -----")
print(raw_request_data)

# decode bytes → string
request = raw_request_data.decode()

#  split the raw request into parts
lines = request.split("\r\n")

print("----- REQUEST LINES -----")
print(lines)
request_line = lines[0]
print("----- REQUEST LINE -----")
print(request_line)

#Finding Where the Blank Line is in the HTTP request Body 
blank_line_index =0
for i in range(len(lines)):
    if lines[i] == "":
        blank_line_index = i
        break

print("----- BLANK LINE INDEX -----")
print(blank_line_index)

#Extracting the Header 
header_lines = lines[1: blank_line_index]
print("----- HEADER LINES -----")
print(header_lines)

#Extracting the Body
body_lines = lines[blank_line_index + 1:]
body = "\r\n".join(body_lines)

print("----- BODY -----")
print(body)

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