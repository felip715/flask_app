from jwt import encode, decode, exceptions
from flask import jsonify
from os import getenv
from datetime import datetime, time, timedelta

def expire_date(days: int):
    now = datetime.now()
    new_date = now + timedelta(days)
    return new_date

def write_token(data: dict):
    token = encode(payload={**data, "exp": expire_date(1)},key=getenv("SECRET"), algorithm="HS256")

    if not isinstance(token, bytes):
        token = token.encode("UTF-8")
    else:
        token = token.decode("UTF-8")
    return token

def validate_token(token, output=False):
    try:
        if output:
            return decode(token, key=getenv("SECRET"), algorithms=["HS256"])
        decode(token, key=getenv("SECRET"), algorithms=["HS256"])
    except exceptions.DecodeError:
        response = jsonify({"message": "Invalid Token"})
        response.status_code = 401
        return response
    except exceptions.ExpiredSignatureError:
        response = jsonify({"message": "Token Expired"})
        response.status_code = 401
        return response