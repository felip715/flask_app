from jwt import encode, decode, exceptions
from flask import jsonify
from os import getenv
from datetime import datetime, time, timedelta

def expire_date(days: int):
    now = datetime.now()
    new_date = now + timedelta(days)
    return new_date

#funcion para describir token
def write_token(data: dict):
    #payload: info a encriptar
    #key: valor para encriptar la info
    token = encode(payload={**data, "exp": expire_date(1)},key=getenv("SECRET"), algorithm="HS256")

    #TODO: CONTROLAR ERROR, genere un validador. Dependiendo de la version de flask puede o no generar un error.
    if not isinstance(token, bytes):
        token = token.encode("UTF-8")
    else:
        token = token.decode("UTF-8")

    return token

#funcion para validar token
def validate_token(token, output=False):
    try:
        if output:
            return decode(token, key=getenv("SECRET"), algorithms=["HS256"])
        decode(token, key=getenv("SECRET"), algorithms=["HS256"])
    #si no se recibe un token, se da la excepcion
    except exceptions.DecodeError:
        response = jsonify({"message": "Invalid Token"})
        response.status_code = 401
        return response
    except exceptions.ExpiredSignatureError:
        response = jsonify({"message": "Token Expired"})
        response.status_code = 401
        return response