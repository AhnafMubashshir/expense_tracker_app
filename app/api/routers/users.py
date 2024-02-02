from fastapi import *
from sqlalchemy import *
from sqlalchemy.orm import *
from ...database import getDB
from typing import List
from app.models.userModel import UserBase, User

router = APIRouter()


@router.post("/create-user/")
def create_user(user: UserBase, db: Session = Depends(getDB)):
    db_user = User(name=user.name, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/users")
def get_all_users(db: Session = Depends(getDB)):

    users = db.query(User).all()

    return {"users": users}
