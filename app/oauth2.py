from threading import stack_size
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# SECRET_KEY
# ALGORITH
# EXPIRATION TIME

SECRET_KEY = "f3956f6dfd481c7383337f0e47dd92c9835f368991e6b9de2224b91e9b4422cf"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict): # Create JWT Token ; data : the data that we want to embed in the token, email here
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) # Add expiration time to the data to be encoded/embeded

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # Encode/Generate the JWT Token using the JWT Token format

    return encoded_jwt

def verify_access_token(token: str, credentials_exception): # Verify token method ; pass in the token, and the exception to throw if the token is invalid
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # Decode the JWT Token recieved

        id: str = payload.get("user_id") # Extract the user id

        if id is None: # IF Id is not found ; raise exception
            raise credentials_exception
        token_data = schemas.TokenData(id=id) # User ID
    except JWTError:
        raise credentials_exception

    return token_data # Return the user ID

def get_current_user(token: str = Depends(oauth2_scheme)): # Pass in the token from the url
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers=({"WWW-Authenticate": "Bearer"}))

    return verify_access_token(token, credentials_exception) # Call verify token method