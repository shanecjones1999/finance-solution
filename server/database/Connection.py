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

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
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

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at_utc = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at_utc = Column(DateTime, default=datetime.utcnow,
                            onupdate=datetime.utcnow, nullable=False)

    plaid_links = relationship('PlaidLink', back_populates='user')


class PlaidLink(Base):
    __tablename__ = 'plaid_links'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    access_token = Column(String, nullable=False)
    item_id = Column(String, unique=True, nullable=False)
    institution_id = Column(String, nullable=True)
    institution_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)

    user = relationship('User', back_populates='plaid_links')


def initialize_database():
    engine = create_engine('sqlite:///db.db', echo=True)
    # Drop existing tables (for development purposes)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)  # Create tables
    return engine


engine = initialize_database()
Session = sessionmaker(bind=engine)
