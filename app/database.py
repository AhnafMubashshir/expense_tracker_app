import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

MYSQL_HOST = '127.0.0.1'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_DB = 'expense_tracker_db'
MYSQL_PORT = os.getenv("MYSQL_PORT")
conn = None


def connect():
    global conn
    conn = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB,
    # port=MYSQL_PORT,
)


    create_table_if_not_exists(
        "user",
        """
        CREATE TABLE IF NOT EXISTS user (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            age INT
        )
    """,
    )

    create_table_if_not_exists(
        "expenditure",
        """
        CREATE TABLE IF NOT EXISTS expenditure (
            expenseID INT AUTO_INCREMENT PRIMARY KEY,
            userID INT,
            date VARCHAR(255),
            time VARCHAR(255),
            event VARCHAR(255),
            details VARCHAR(255),
            expense FLOAT,
            FOREIGN KEY (userID) REFERENCES user(id)
        )
    """,
    )

    return conn


def create_table_if_not_exists(table_name, create_table_query):
    cursor = conn.cursor()

    # print(f"Executing query for table {table_name}:\n{create_table_query}")

    try:
        cursor.execute(create_table_query)

        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()


def getConnection():
    return conn
