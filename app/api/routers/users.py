from fastapi import APIRouter, HTTPException
from ...models.userModel import UpdateUserRequest, UpdateUserResponse, User, RegisteredUser
from ...database import getConnection
from typing import List

router = APIRouter()


@router.post("/create-user/", response_model=User)
def create_user(user: User):
    conn = getConnection()
    cursor = conn.cursor()
    query = "INSERT INTO user (name, email, age) VALUES (%s, %s, %s)"
    cursor.execute(query, (user.name, user.email, user.age))
    conn.commit()
    cursor.close()
    return user


@router.get("/user/{user_id}", response_model=RegisteredUser)
def get_user_by_id(user_id: int):
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT id, name, email, age FROM user WHERE id = %s"
    cursor.execute(query, (user_id,))

    user_data = cursor.fetchone()

    cursor.close()

    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")

    return User(**user_data)


@router.delete("/user/{user_id}", response_model=dict)
def delete_user_by_id(user_id: int):
    conn = getConnection()
    cursor = conn.cursor()

    query = "DELETE FROM user WHERE id = %s"
    cursor.execute(query, (user_id,))

    conn.commit()
    cursor.close()

    return {"message": "User deleted successfully"}


@router.get("/users", response_model=List[RegisteredUser])
def get_all_users():
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT id, name, email, age FROM user"
    cursor.execute(query)

    user_data_list = cursor.fetchall()

    cursor.close()

    return user_data_list


@router.put("/update-user/{user_id}", response_model=UpdateUserResponse)
def update_user(user_id: int, updated_user: UpdateUserRequest):
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)

    # Check if the user exists
    check_query = "SELECT id FROM user WHERE id = %s"
    cursor.execute(check_query, (user_id,))
    existing_user = cursor.fetchone()

    if existing_user is None:
        cursor.close()
        raise HTTPException(status_code=404, detail="User not found")

    # Construct the update query dynamically based on the provided fields
    update_query = "UPDATE user SET "
    update_data = []

    if updated_user.name is not None:
        update_query += "name=%s, "
        update_data.append(updated_user.name)

    if updated_user.email is not None:
        update_query += "email=%s, "
        update_data.append(updated_user.email)

    if updated_user.age is not None:
        update_query += "age=%s, "
        update_data.append(updated_user.age)

    update_query = update_query.rstrip(", ")

    update_query += " WHERE id=%s"
    update_data.append(user_id)

    cursor.execute(update_query, tuple(update_data))

    conn.commit()

    get_user_query = "SELECT id, name, email, age FROM user WHERE id = %s"
    cursor.execute(get_user_query, (user_id,))
    updated_user_data = cursor.fetchone()

    cursor.close()

    return UpdateUserResponse(**updated_user_data)