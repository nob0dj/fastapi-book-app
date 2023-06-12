from datetime import datetime

import jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import ExpiredSignatureError

from config import configs


def decode_jwt(token) -> dict:
    """
    token을 decode하여 반환함, decode에 실패하는 경우 payload = None으로 반환
    :param token:
    :return:
    """
    payload = jwt.decode(token, configs.JWT_SECRET_KEY, configs.JWT_ALGORITHM)
    # datetime#utcnow():datetime
    # datetime#timestamp():float
    if payload['exp'] < int(datetime.utcnow().timestamp()):  # 토큰이 만료된 경우
        raise ExpiredSignatureError
    return payload


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        """
        :param request: fastapi.Request (starlette.requests)
        :return:
        """
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        print(
            credentials)  # scheme='Bearer' credentials='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJob25nZ2QiLCJncmFkZSI6IkJBU0lDIiwiZXhwIjoxNjg1ODY1MTA5fQ.dxqUaVjRCFQwNXctkzoaBb-7pihnzbELSQ_m6e9e0ms'
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        is_token_valid: bool = False

        try:
            payload = decode_jwt(jwtoken)
        except:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid
