# from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
# from sqlalchemy.orm import relationship
# from datetime import datetime
# from database.Connection import Base


# class PlaidLink(Base):
#     __tablename__ = 'plaid_links'

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
#     access_token = Column(String, nullable=False)
#     item_id = Column(String, unique=True, nullable=False)
#     institution_id = Column(String, nullable=True)
#     institution_name = Column(String, nullable=True)
#     created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
#     updated_at = Column(DateTime, default=datetime.utcnow,
#                         onupdate=datetime.utcnow, nullable=False)

#     user = relationship('User', back_populates='plaid_links')
