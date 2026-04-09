import socket
from request import parse_request
from router import route_request
from response import build_response
from datetime import datetime

host = "127.0.0.1"
port = 8080


def accept_connection(server_socket):
    connection_socket, client_address = server_socket.accept()
    print(f"Connection accepted from {client_address}")
    return connection_socket, client_address


def read_request(connection_socket):
    raw_request_data = connection_socket.recv(1024)

    while b"\r\n\r\n" not in raw_request_data:
        more_data = connection_socket.recv(1024)
        if not more_data:
            break
        raw_request_data += more_data

    header_part, separator, body_part = raw_request_data.partition(b"\r\n\r\n")
    headers_text = header_part.decode()

    content_length = 0
    header_lines = headers_text.split("\r\n")

    for line in header_lines:
        if line.lower().startswith("content-length:"):
            content_length = int(line.split(":", 1)[1].strip())
            break

    while len(body_part) < content_length:
        more_body_data = connection_socket.recv(1024)
        if not more_body_data:
            break
        body_part += more_body_data

    raw_request_data = header_part + separator + body_part

    print("----- RAW HTTP REQUEST -----")
    print(raw_request_data)

    request_text = raw_request_data.decode()
    return request_text

def log_request(request_data, malformed_request, status_code):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if malformed_request:
        print(f"[{timestamp}] MALFORMED_REQUEST -> {status_code}")
    else:
        method = request_data["method"]
        path = request_data["path"]
        print(f"[{timestamp}] {method} {path} -> {status_code}")

def send_response(connection_socket, response):
    connection_socket.send(response.encode())

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))
server_socket.listen()

print(f"Server is listening on {host}:{port}")

try:
    while True:
        connection_socket, client_address = accept_connection(server_socket)
        request_text = read_request(connection_socket)
        request_data, malformed_request = parse_request(request_text)
        status_code, content_type, response_body = route_request(request_data, malformed_request)

        log_request(request_data, malformed_request, status_code)

        response = build_response(status_code, content_type, response_body)
        send_response(connection_socket, response)

        connection_socket.close()

except KeyboardInterrupt:
    print("\nServer stopped by user.")

finally:
    server_socket.close()