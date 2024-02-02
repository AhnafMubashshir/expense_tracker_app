from fastapi import APIRouter, HTTPException
from ...models.expenseModel import Expenditure
from ...database import getConnection

router = APIRouter()

@router.post("/create-expense/", response_model=Expenditure)
def create_expense(expense: Expenditure):
    conn = getConnection()
    cursor = conn.cursor()

    try:
        query = """
            INSERT INTO expenditure 
            (expenseID, userID, date, time, event, details, expense) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            expense.expenseID, expense.userID, expense.date,
            expense.time, expense.event, expense.details, expense.expense
        ))
        conn.commit()
        expense_id = cursor.lastrowid
        expense.expenseID = expense_id
        return expense

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
