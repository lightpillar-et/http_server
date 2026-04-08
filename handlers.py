def handle_home():
    return 200, "text/plain", "Home route"


def handle_about():
    return 200, "text/plain", "About route"


def handle_api_hello():
    return 200, "application/json", '{"message": "Hello"}'


def handle_not_found():
    return 404, "text/plain", "Not Found"


def handle_bad_request():
    return 400, "text/plain", "Bad Request"