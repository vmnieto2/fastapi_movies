from jwt import encode, decode

def create_token(data: dict):

    token = encode(payload=data, key="v1c704_k3y", algorithm="HS256")
    return token

def validate_token(token: str) -> dict:
    data: dict = decode(token, key="v1c704_k3y", algorithms=["HS256"])
    return data
