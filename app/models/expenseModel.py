from pydantic import BaseModel

class Expenditure(BaseModel):
    userID: str
    date: str
    time: str
    event: str
    details: str
    expense: float

