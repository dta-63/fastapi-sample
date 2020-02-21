import os
import requests 

from typing import Dict, List, Optional, Any
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, jwk, JWTError
from jose.utils import base64url_decode
from pydantic import BaseModel
from starlette.requests import Request

url = "{}/realms/{}/protocol/openid-connect".format(
    os.getenv('SSO_URL'),
    os.getenv('SSO_REALM')
)

JWK = Dict[str, str]


class JWKS(BaseModel):
    keys: List[JWK]


class User(BaseModel):
    name: str
    preferred_username: str
    given_name: str
    locale: str
    family_name: str
    email: str
    realm_access: Any
    resource_access: Any


class Auth(OAuth2PasswordBearer):
    def __init__(self, *, roles: Optional[List[str]] = []):
        self.roles = set(roles)
        super().__init__(tokenUrl="{}/token".format(url))

    def __call__(self, request: Request) -> User:
        unauthorized = HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        forbidden = HTTPException(
            status_code=403,
            detail="Forbidden",
            headers={"WWW-Authenticate": "Bearer"},
        )

        authorization: str = request.headers.get("Authorization")
        if authorization is None:
            raise unauthorized
        scheme, _, token = authorization.partition(" ")
        try:
            jwks = requests.get("{}/certs".format(url)).json()
            valid = self.verify_jwt(token, jwks)
            if valid:
                user = User(**jwt.get_unverified_claims(token))
            else:
                raise unauthorized
            if len(self.roles) > 0:
                # Check roles using token informations
                roles = user.realm_access['roles']
                client_id = os.getenv('SSO_CLIENT')
                if client_id is not None and user.resource_access[client_id]:
                    roles = roles + user.resource_access[client_id]['roles']

                valid = len(list(set(roles) & set(self.roles)))
                if not valid:
                    raise forbidden
        except JWTError:
            raise unauthorized
        return user

    def get_hmac_key(self, token: str, jwks: JWKS) -> Optional[JWK]:
        kid = jwt.get_unverified_header(token).get("kid")
        for key in jwks.get("keys", []):
            if key.get("kid") == kid:
                return key

    def verify_jwt(self, token: str, jwks: JWKS) -> bool:
        hmac_key = self.get_hmac_key(token, jwks)

        if not hmac_key:
            raise ValueError("No pubic key found!")

        hmac_key = jwk.construct(hmac_key)

        message, encoded_signature = token.rsplit(".", 1)
        decoded_signature = base64url_decode(encoded_signature.encode())

        return hmac_key.verify(message.encode(), decoded_signature)
