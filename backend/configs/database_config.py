import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import mysql.connector



# Lod the environment variables
load_dotenv()

username = os.environ['DATABASE_USERNAME']
database = os.environ['DATABASE_NAME']
database_type = os.environ['DATABASE_TYPE']
host = os.environ['DATABASE_HOST']
password = os.environ['DATABASE_PASSWORD']
port = os.environ.get('DATABASE_PORT', 5432)



db_url = f"{database_type}://{username}:{password}@{host}:{port}/{database}"
print(db_url)

engine = create_engine(db_url,)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
