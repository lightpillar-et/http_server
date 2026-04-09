from handlers import (
    handle_home,
    handle_about,
    handle_api_hello,
    handle_not_found,
    handle_bad_request,
    handle_echo
)


def route_request(request_data, malformed_request):
    if malformed_request:
        return handle_bad_request()

    method = request_data["method"]
    path = request_data["path"]

    if method == "GET" and path == "/":
        return handle_home()

    elif method == "GET" and path == "/about":
        return handle_about()

    elif method == "GET" and path == "/api/hello":
        return handle_api_hello()
    
    elif method == "POST" and path == "/echo":
        return handle_echo(request_data)

    else:
        return handle_not_found()