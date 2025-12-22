from flask import request


def get_current_user_id():
    user_id = request.headers.get("X-User-ID")
    if user_id:
        return int(user_id)
    return 1
