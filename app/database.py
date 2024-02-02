from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# load_dotenv()

# MYSQL_HOST = '127.0.0.1'
# MYSQL_USER = 'root'
# MYSQL_PASSWORD = 'root'
# MYSQL_DB = 'expense_tracker_db'
# MYSQL_PORT = os.getenv("MYSQL_PORT")
sessionLocal = None
Base = declarative_base()

def connect():
    global sessionLocal
    engine = create_engine("mysql+mysqlconnector://root:root@127.0.0.1:3306/expense_tracker_db")
    sessionLocal = sessionmaker(engine)
    Base.metadata.create_all(engine)

    return sessionLocal()


def getDB():
    db = sessionLocal()

    try:
        yield db
    finally:
        db.close()
