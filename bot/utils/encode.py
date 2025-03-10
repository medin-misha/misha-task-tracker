import base64


def base_encode(user_name: str, user_id: str) -> str:
    string: str = f"{user_name}:{user_id}"
    str_bytes: bytes = string.encode("ascii")
    str_base64: str = base64.b64encode(str_bytes).decode("ascii")
    return str_base64
