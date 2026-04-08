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