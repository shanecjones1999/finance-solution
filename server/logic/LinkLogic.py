from database.Connection import PlaidLink
from logic.BaseLogic import BaseLogic
import os
import plaid
from plaid.api import plaid_api

from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.item_get_request import ItemGetRequest
from plaid.model.institutions_get_by_id_request import InstitutionsGetByIdRequest
from plaid.model.country_code import CountryCode


class LinkLogic(BaseLogic):
    def __init__(self):
        super().__init__()
        # Fill in your Plaid API keys - https://dashboard.plaid.com/account/keys
        PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
        PLAID_SECRET = os.getenv('PLAID_SECRET')
        # Use 'sandbox' to test with Plaid's Sandbox environment (username: user_good,
        # password: pass_good)
        # Use `development` to test with live users and credentials and `production`
        # to go live
        PLAID_ENV = os.getenv('PLAID_ENV', 'sandbox')
        # PLAID_PRODUCTS is a comma-separated list of products to use when initializing
        # Link. Note that this list must contain 'assets' in order for the app to be
        # able to create and retrieve asset reports.
        PLAID_PRODUCTS = os.getenv('PLAID_PRODUCTS', 'transactions').split(',')

        # PLAID_COUNTRY_CODES is a comma-separated list of countries for which users
        # will be able to select institutions from.
        PLAID_COUNTRY_CODES = os.getenv('PLAID_COUNTRY_CODES', 'US').split(',')

        host = plaid.Environment.Sandbox

        if PLAID_ENV == 'sandbox':
            host = plaid.Environment.Sandbox

        if PLAID_ENV == 'development':
            host = plaid.Environment.Development

        if PLAID_ENV == 'production':
            host = plaid.Environment.Production

        configuration = plaid.Configuration(
            host=host,
            api_key={
                'clientId': PLAID_CLIENT_ID,
                'secret': PLAID_SECRET,
                'plaidVersion': '2020-09-14'
            }
        )

        self.country_codes = PLAID_COUNTRY_CODES

        api_client = plaid.ApiClient(configuration)
        self.client = plaid_api.PlaidApi(api_client)

    def get_transactions(self, user_id):
        cursor = ''
        added = []
        modified = []
        removed = []
        has_more = True
        try:
            plaid_link = self.get_plaid_links_by_user_id(user_id=user_id)
            access_token = plaid_link.access_token

            # Iterate through each page of new transaction updates for item
            while has_more:
                request = TransactionsSyncRequest(
                    access_token=access_token,
                    cursor=cursor,
                )
                response = self.client.transactions_sync(request).to_dict()
                # Add this page of results
                added.extend(response['added'])
                modified.extend(response['modified'])
                removed.extend(response['removed'])
                has_more = response['has_more']
                # Update cursor to the next cursor
                cursor = response['next_cursor']

            # Return the 8 most recent transactions
            latest_transactions = sorted(
                added, key=lambda t: t['date'])  # [-8:]
            for index, transaction in enumerate(latest_transactions, start=1):
                transaction['id'] = index  # Assigning a simple incremental id

            return latest_transactions, ""
            # return jsonify({
            #     'data': latest_transactions})

        except Exception:
            # error_response = format_error(e)
            # return jsonify(error_response)
            return [], "Error looking up transations"

    def get_access_token(self, public_token, user_id):
        try:
            exchange_request = {'public_token': public_token}

            exchange_response = self.client.item_public_token_exchange(
                exchange_request)
            access_token = exchange_response['access_token']
            item_id = exchange_response['item_id']

            institution_response, _ = self.get_institution_and_item(
                access_token)

            institution_id = institution_response['institution']['institution_id']
            institution_name = institution_response['institution']['name']

            self.store_plaid_link(
                user_id, access_token, item_id, institution_id, institution_name)
            return exchange_response, ""
        except Exception as e:
            return None, f"Error: {e}"

    def get_plaid_links_by_user_id(self, user_id) -> PlaidLink:
        return self.session.query(PlaidLink).filter(PlaidLink.user_id == user_id)

    def get_item(self, user_id):
        res = []
        try:
            plaid_link = self.get_plaid_links_by_user_id(user_id=user_id)

            for link in plaid_link:
                access_token = link.access_token

                institution_response, response = self.get_institution_and_item(
                    access_token)

                item = {'item': response.to_dict()['item'],
                        'institution': institution_response.to_dict()['institution']
                        }
                res.append(item)

            return res, ""
        except Exception as e:
            return res, f"Error getting item: {e}"

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
