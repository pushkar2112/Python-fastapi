from jose import JWTError, jwt
from datetime import datetime, timedelta

# SECRET_KEY
# ALGORITH
# EXPIRATION TIME

SECRET_KEY = "f3956f6dfd481c7383337f0e47dd92c9835f368991e6b9de2224b91e9b4422cf"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt