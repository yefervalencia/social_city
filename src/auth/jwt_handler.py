import bcrypt
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException,status,Depends
from datetime import (
 datetime,
 timezone,
 timedelta,
)
from src.repositories.user import UserRepository
class JWTHandler:
    def __init__(self, secret, algorithm)  -> None:
        self.secret = secret
        self.algorithm = algorithm
        
    def verify_admin(self,credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        token = credentials.credentials
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            rol: str = payload.get("user.rol")
            if rol is None:
                raise credentials_exception
            if rol != "admin":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        except jwt.InvalidSignatureError:
            raise credentials_exception
        return token
            

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password=password.encode("utf-8"),
            salt=bcrypt.gensalt())

    def verify_password(self,
        password: str,
        hashed_password: str) -> bool:
        print(password)
        print(hashed_password.encode("utf-8"))
        return bcrypt.checkpw(
        password=password.encode("utf-8") ,
        hashed_password=hashed_password.encode("utf-8"),
        )

    def encode_token(self, user):
        payload = {
        # exp (expiration time): Time after which the JWT expires
        "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=30),
        # iat (issued at time): Time at which the JWT was issued
        "iat": datetime.now(tz=timezone.utc),
        # sub (subject): Subject of the JWT (the user)
        "sub": user.email,
        # Custom Issues
        "scope": "access_token",
        "user.name": user.name,
        "user.id": user.id,
        "user.rol": user.rol,
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def decode_token(self, token):
        try:
            payload = jwt.decode(token,
            self.secret,
            algorithms=[self.algorithm])
            if payload["scope"] == "access_token":
                return payload
            raise HTTPException(
        status_code=401,
        detail="Scope for the token is invalid"
        )
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        
    def encode_refresh_token(self, user):
        payload = {
        "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=30),
        "iat": datetime.now(tz=timezone.utc),
        "scope": "refresh_token",
        "sub": user.email,
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def refresh_token(self, refresh_token):
        try:
            payload = jwt.decode(
                refresh_token, self.secret, algorithms=[self.algorithm]
        )
            if payload and payload["scope"] == "refresh_token":
                user = UserRepository.get_user(payload["sub"])
                new_token = self.encode_token(user)
                return new_token
            raise HTTPException(status_code=401, detail="Invalid scope for token")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Refresh token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

