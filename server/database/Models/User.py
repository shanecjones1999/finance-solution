# from sqlalchemy import Column, Integer, String, DateTime
# from sqlalchemy.orm import relationship
# from datetime import datetime
# from database.Connection import Base


# class User(Base):
#     __tablename__ = 'users'

#     user_id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, nullable=False)
#     password = Column(String, nullable=False)
#     created_at_utc = Column(DateTime, default=datetime.utcnow, nullable=False)
#     updated_at_utc = Column(DateTime, default=datetime.utcnow,
#                             onupdate=datetime.utcnow, nullable=False)

# plaid_links = relationship('PlaidLink', back_populates='user')
