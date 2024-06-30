# from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
# from sqlalchemy.orm import relationship
# from datetime import datetime
# from server.database.Connection import Base


# class Transaction(Base):
#     __tablename__ = 'transactions'

#     id = Column(Integer, primary_key=True, index=True)
#     plaid_link_id = Column(Integer, ForeignKey(
#         'plaid_links.id'), nullable=False)
#     account_id = Column(String, nullable=False)
#     amount = Column(Float, nullable=False)
#     date = Column(DateTime, nullable=False)
#     category = Column(String, nullable=True)
#     merchant_name = Column(String, nullable=True)
#     created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

#     plaid_link = relationship('PlaidLink', back_populates='transactions')
