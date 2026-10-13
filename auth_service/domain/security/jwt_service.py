from datetime import datetime, timedelta, timezone

import jwt
from domain.models import UserResponse


class JWTService:
    def __init__(self, secret_key: str, lifetime: int) -> None:
        self.secret_key = secret_key
        self.algorithm = "HS256"
        self.lifetime = lifetime


    def create_token(self, user: UserResponse):
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.lifetime)
        payload = {'sub': str(user.id), 'email': user.email, 'exp': expire}
        token = jwt.encode(payload, self.secret_key, self.algorithm)

        return token


    def verify_token(self, token: str):
        payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

        return payload
