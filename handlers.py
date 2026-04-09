def handle_home():
    with open("index.html", "r") as file:
        html_content = file.read()
    return 200, "text/html", html_content


def handle_about():
    with open("about.html", "r") as file:
        html_content = file.read()
    return 200, "text/html", html_content


def handle_api_hello():
    return 200, "application/json", '{"message": "Hello"}'


def handle_not_found():
    with open("404.html", "r") as file:
        html_content = file.read()
    return 404, "text/html", html_content


def handle_bad_request():
    return 400, "text/plain", "Bad Request"


def handle_echo(request_data):
    return 200, "text/plain", request_data["body"]