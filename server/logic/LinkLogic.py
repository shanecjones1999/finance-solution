# server/logic/plaid_logic.py
from database.Connection import Session, PlaidLink
# from database.Models.PlaidLink import PlaidLink


class LinkLogic:
    def __init__(self):
        self.session = Session()

    def store_plaid_link(self, user_id, access_token, item_id, institution_id, institution_name):
        plaid_link = PlaidLink(
            user_id=user_id,
            access_token=access_token,
            item_id=item_id,
            institution_id=institution_id,
            institution_name=institution_name
        )
        self.session.add(plaid_link)
        self.session.commit()

    def close_session(self):
        self.session.close()
