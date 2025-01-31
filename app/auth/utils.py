'''
This file contains the utils for the auth module.
'''

from fastapi import Request
import time

def verify_session(request: Request) -> bool:
    user_info = request.session.get("user_info")
    if user_info and "expires_in_timestamp" in user_info:
        return user_info["expires_in_timestamp"] > time.time()
    return False


