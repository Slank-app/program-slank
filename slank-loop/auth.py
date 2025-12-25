from flask import request


def get_current_user():
    user_id = request.headers.get("X-User-ID")
    if user_id:
        return int(user_id)
    return 1


def get_current_goal():
    goal_id = request.headers.get("X-Goal-ID")
    if goal_id:
        return int(goal_id)
    return 1
