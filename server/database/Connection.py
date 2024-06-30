# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# # Define the SQLite database URL
# DATABASE_URL = 'sqlite:///server/db.db'

# # Create the SQLAlchemy engine
# engine = create_engine(DATABASE_URL, echo=True)

# # Create a configured "Session" class
# Session = sessionmaker(bind=engine)

# # Create a Base class for our class definitions
# Base = declarative_base()

# database/connection.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
# from database.Connection import Base

Base = declarative_base()

# from sqlalchemy import Column, Integer, String, DateTime
# from sqlalchemy.orm import relationship
# from datetime import datetime
# from database.Connection import Base


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at_utc = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at_utc = Column(DateTime, default=datetime.utcnow,
                            onupdate=datetime.utcnow, nullable=False)


def initialize_database():
    engine = create_engine('sqlite:///db.db', echo=True)
    # Drop existing tables (for development purposes)
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)  # Create tables
    return engine


engine = initialize_database()
Session = sessionmaker(bind=engine)
