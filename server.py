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

#----- HTTP Request Parsing-----
lines = request.split("\r\n")

print("----- REQUEST LINES -----")
print(lines)
request_line = lines[0]
print("----- REQUEST LINE -----")
print(request_line)
method = ""
path = ""
version = ""
malformed_request = False
if request_line == "":
    print("Error: Request line is missing")
    malformed_request = True
else:
    
    request_line_parts = request_line.split()

    print("----- REQUEST LINE PARTS -----")
    print(request_line_parts)
    if len(request_line_parts) != 3:
        print("Error: Malformed request line")
        malformed_request = True
    else:
        method = request_line_parts[0]
        path = request_line_parts[1]
        version = request_line_parts[2]

        print("----- PARSED REQUEST LINE -----")
        print("Method:", method)
        print("Path:", path)
        print("Version:", version)



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
# Turning the Header into Dictionarry
headers = {}
for header_line in header_lines:
    if ":" in header_line:
        name, value = header_line.split(":", 1)
        headers[name] = value.strip()

print("Host:", headers.get("Host"))
print("User-Agent:", headers.get("User-Agent"))
print("Accept:", headers.get("Accept"))

#Extracting the Body
body_lines = lines[blank_line_index + 1:]
body = "\r\n".join(body_lines)

print("----- BODY -----")
print(body)

#Create request data structure
request_data = {
    "method": method,
    "path": path,
    "version": version,
    "headers": headers,
    "body": body
}

print("----- REQUEST DATA STRUCTURE -----")
print(request_data) 
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