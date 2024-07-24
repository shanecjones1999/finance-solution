from Plaid.PlaidConfiguration import PlaidConfiguration
from database.Connection import PlaidLink

from Models.Plaid.FinancialInstitution import FinancialInstitution
from Models.Plaid.FinancialItem import FinancialItem
from Models.Plaid.FinancialInstitutionItem import FinancialInstitutionItem

from database.Connection import Session

import plaid
from plaid.api import plaid_api

from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.item_get_request import ItemGetRequest
from plaid.model.institutions_get_by_id_request import InstitutionsGetByIdRequest
from plaid.model.country_code import CountryCode


#  Wrapper class for Plaid API. We should use this class to interact with Plaid.
class PlaidApiWrapper:
    def __init__(self):
        config = PlaidConfiguration()

        self.country_codes = config.get_country_codes()

        api_client = plaid.ApiClient(config.get_configuration())
        self.client = plaid_api.PlaidApi(api_client)

        self.session = Session()

    def get_financial_items(self, user_id):
        res = []
        try:
            plaid_link = self.get_plaid_links_by_user_id(user_id=user_id)

            for link in plaid_link:
                access_token = link.access_token

                institution_response, response = self.get_institution_and_item(
                    access_token)

                institution = institution_response.to_dict()['institution']
                item = response.to_dict()['item']
                value = {'institution': institution, 'item': item}

                res.append(value)

            return res, ""
        except Exception as e:
            return res, f"Error getting item: {e}"

    def get_plaid_links_by_user_id(self, user_id) -> PlaidLink:
        return self.session.query(PlaidLink).filter(PlaidLink.user_id == user_id)

    def get_institution_and_item(self, access_token):
        request = ItemGetRequest(access_token=access_token)
        response = self.client.item_get(request)
        request = InstitutionsGetByIdRequest(
            institution_id=response['item']['institution_id'],
            country_codes=list(
                map(lambda x: CountryCode(x), self.country_codes))
        )
        institution_response = self.client.institutions_get_by_id(
            request)

        return institution_response, response
