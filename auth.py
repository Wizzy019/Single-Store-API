from datetime import datetime, timezone, timedelta
from jose import jwt
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

load_dotenv()

SECRETE_KEY = os.getenv("SECRETE_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCES_TOKEN_EXPIRE_MUNITES=30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# hash password
def hash_password(password: str):
    max_lent = 72
    return pwd_context.hash(password[:max_lent])

# verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# access token fxn
def create_acces_token(data:dict):
    to_encode = data.copy
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCES_TOKEN_EXPIRE_MUNITES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, SECRETE_KEY, algorithm=ALGORITHM)