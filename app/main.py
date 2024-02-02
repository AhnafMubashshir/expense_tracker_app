from fastapi import FastAPI
import uvicorn
from .api.routers import users, expenses
from .database import connect

app = FastAPI()
conn = connect()

app.include_router(users.router)
# app.include_router(expenses.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


if __name__ == "__main__":
    uvicorn.run(app, port=5000)
