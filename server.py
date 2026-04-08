import socket
from request import parse_request
from router import route_request
from response import build_response

host = "127.0.0.1"
port = 8080


def accept_connection(server_socket):
    connection_socket, client_address = server_socket.accept()
    print(f"Connection accepted from {client_address}")
    return connection_socket, client_address


def read_request(connection_socket):
    raw_request_data = connection_socket.recv(1024)

    print("----- RAW HTTP REQUEST -----")
    print(raw_request_data)

    request_text = raw_request_data.decode()
    return request_text


def send_response(connection_socket, response):
    connection_socket.send(response.encode())


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

print(f"Server is listening on {host}:{port}")

connection_socket, client_address = accept_connection(server_socket)
request_text = read_request(connection_socket)
request_data, malformed_request = parse_request(request_text)
status_code, content_type, response_body = route_request(request_data, malformed_request)
response = build_response(status_code, content_type, response_body)
send_response(connection_socket, response)

connection_socket.close()
server_socket.close()