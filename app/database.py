from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHMEY_DATABASE_URL = 'postgresql://postgres:pass%40123@localhost/fastapi'

engine = create_engine(SQLALCHMEY_DATABASE_URL)

sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

