import socket

host = "127.0.0.1"
port = 8080

# -------------------- STATUS CODE --------------------
status_reasons = {
    200: "OK",
    404: "Not Found",
    400: "Bad Request"
}


# -------------------- ACCEPT CONNECTION --------------------
def accept_connection(server_socket):
    connection_socket, client_address = server_socket.accept()
    print(f"Connection accepted from {client_address}")
    print(f"Connection Soket {connection_socket}")
    return connection_socket, client_address


# -------------------- READ REQUEST --------------------
def read_request(connection_socket):
    raw_request_data = connection_socket.recv(1024)

    print("----- RAW HTTP REQUEST -----")
    print(raw_request_data)

    request_text = raw_request_data.decode()
    return request_text


# -------------------- PARSE REQUEST --------------------
def parse_request(request_text):
    lines = request_text.split("\r\n")

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

    blank_line_index = 0
    for i in range(len(lines)):
        if lines[i] == "":
            blank_line_index = i
            break

    print("----- BLANK LINE INDEX -----")
    print(blank_line_index)

    header_lines = lines[1:blank_line_index]
    print("----- HEADER LINES -----")
    print(header_lines)

    headers = {}
    for header_line in header_lines:
        if ":" in header_line:
            name, value = header_line.split(":", 1)
            headers[name] = value.strip()

    print("Host:", headers.get("Host"))
    print("User-Agent:", headers.get("User-Agent"))
    print("Accept:", headers.get("Accept"))

    body_lines = lines[blank_line_index + 1:]
    body = "\r\n".join(body_lines)

    print("----- BODY -----")
    print(body)

    request_data = {
        "method": method,
        "path": path,
        "version": version,
        "headers": headers,
        "body": body
    }

    print("----- REQUEST DATA STRUCTURE -----")
    print(request_data)

    return request_data, malformed_request


# -------------------- ROUTE REQUEST --------------------
def route_request(request_data, malformed_request):
    if malformed_request:
        return 400, "text/plain", "Bad Request"

    method = request_data["method"]
    path = request_data["path"]

    if method == "GET" and path == "/":
        return 200, "text/plain", "Home route"

    elif method == "GET" and path == "/about":
        return 200, "text/plain", "About route"

    elif method == "GET" and path == "/api/hello":
        return 200, "application/json", '{"message": "Hello"}'

    else:
        return 404, "text/plain", "Not Found"


# -------------------- BUILD RESPONSE --------------------
def build_response(status_code, content_type, response_body):
    version = "HTTP/1.1"
    reason_phrase = status_reasons[status_code]
    status_line = f"{version} {status_code} {reason_phrase}"

    response = (
        f"{status_line}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(response_body)}\r\n"
        "\r\n"
        f"{response_body}"
    )

    return response


# -------------------- SEND RESPONSE --------------------
def send_response(connection_socket, response):
    connection_socket.send(response.encode())


# -------------------- MAIN SERVER FLOW --------------------
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