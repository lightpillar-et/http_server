status_reasons = {
    200: "OK",
    404: "Not Found",
    400: "Bad Request"
}


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