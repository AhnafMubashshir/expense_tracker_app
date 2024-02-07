import os
from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ...database import getDB
from app.models.userModel import UserBase, User
from fastapi.encoders import jsonable_encoder
from passlib.context import *
from ...interfaces.users import LoginCredentials
from dotenv import load_dotenv
from jose import jwt

router = APIRouter()
load_dotenv()
jwt_secretKey = os.getenv("JWT_SECRET_KEY")
algorithm = os.getenv("ALGORITHM")

ACCESS_TOKEN = ""

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def generateToken(user: User):
    global ACCESS_TOKEN
    try: 

        user_dict = jsonable_encoder(user)
        ACCESS_TOKEN = jwt.encode({"user": user_dict}, jwt_secretKey, algorithm)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/register-user")
def create_user(user: UserBase, db: Session = Depends(getDB)):
    try:
        hashedPassword = crypt.hash(user.password)
        db_user = User(name=user.name, email=user.email, password=hashedPassword)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/users")
def get_all_users(db: Session = Depends(getDB)):
    try:
        users = db.query(User).all()
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete-users")
def delete_all_users(db: Session = Depends(getDB)):
    try:
        db.query(User).delete()
        db.commit()
        return {"message": "All users deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete-user-by-id/{user_id}")
def delete_user_by_id(user_id: int, db: Session = Depends(getDB)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(user)
        db.commit()
        return {"message": f"User with ID {user_id} deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login-user")
def login(login_credentials: LoginCredentials, db: Session = Depends(getDB)):
    user = db.query(User).filter(User.email == login_credentials.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    else:
        verified = crypt.verify(login_credentials.password, user.password)

        if verified:
            generateToken(user)
            return {ACCESS_TOKEN}
        else:
            raise HTTPException(status_code=401, detail="Wrong credentials")
        

@router.delete('/delete-profile')
def delete_profile(db: Session = Depends(getDB), token: str = Depends(oauth2_scheme)):
    current_user = jwt.decode(token, jwt_secretKey, algorithms=[algorithm])

    if not current_user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # # Get the user from the database based on the decoded token
    # user = db.query(User).filter(User.email == current_user['email']).first()

    # if not user:
    #     raise HTTPException(status_code=404, detail="User not found")

    # # Your logic to delete the user's profile goes here
    # db.delete(user)
    # db.commit()

    return {"message": current_user}

@router.post("/token")
def login_for_token(
    login_credentials: LoginCredentials = Depends(LoginCredentials),
    db: Session = Depends(getDB),
):
    user = db.query(User).filter(User.email == login_credentials.username).first()

    if not user or not user.verify_password(login_credentials.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    generateToken(user)
    return {"access_token": ACCESS_TOKEN, "token_type": "bearer"}
