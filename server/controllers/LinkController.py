from flask import Blueprint, request, jsonify, session
from flask.views import MethodView

from logic.LinkLogic import LinkLogic
from utils.AuthUtils import AuthUtils
from Authorization.TokenValidation import token_required

import base64
import os
import datetime as dt
import json
import time
from datetime import date, timedelta

from dotenv import load_dotenv
import plaid
from plaid.model.payment_amount import PaymentAmount
from plaid.model.payment_amount_currency import PaymentAmountCurrency
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.recipient_bacs_nullable import RecipientBACSNullable
from plaid.model.payment_initiation_address import PaymentInitiationAddress
from plaid.model.payment_initiation_recipient_create_request import PaymentInitiationRecipientCreateRequest
from plaid.model.payment_initiation_payment_create_request import PaymentInitiationPaymentCreateRequest
from plaid.model.payment_initiation_payment_get_request import PaymentInitiationPaymentGetRequest
from plaid.model.link_token_create_request_payment_initiation import LinkTokenCreateRequestPaymentInitiation
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.asset_report_create_request import AssetReportCreateRequest
from plaid.model.asset_report_create_request_options import AssetReportCreateRequestOptions
from plaid.model.asset_report_user import AssetReportUser
from plaid.model.asset_report_get_request import AssetReportGetRequest
from plaid.model.asset_report_pdf_get_request import AssetReportPDFGetRequest
from plaid.model.auth_get_request import AuthGetRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.identity_get_request import IdentityGetRequest
from plaid.model.investments_transactions_get_request_options import InvestmentsTransactionsGetRequestOptions
from plaid.model.investments_transactions_get_request import InvestmentsTransactionsGetRequest
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.investments_holdings_get_request import InvestmentsHoldingsGetRequest


from plaid.model.transfer_authorization_create_request import TransferAuthorizationCreateRequest
from plaid.model.transfer_create_request import TransferCreateRequest
from plaid.model.transfer_get_request import TransferGetRequest
from plaid.model.transfer_network import TransferNetwork
from plaid.model.transfer_type import TransferType
from plaid.model.transfer_authorization_user_in_request import TransferAuthorizationUserInRequest
from plaid.model.ach_class import ACHClass
from plaid.model.transfer_create_idempotency_key import TransferCreateIdempotencyKey
from plaid.model.transfer_user_address_in_request import TransferUserAddressInRequest
from plaid.model.signal_evaluate_request import SignalEvaluateRequest
from plaid.model.statements_list_request import StatementsListRequest
from plaid.model.link_token_create_request_statements import LinkTokenCreateRequestStatements
from plaid.model.statements_download_request import StatementsDownloadRequest
from plaid.api import plaid_api

load_dotenv()

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

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

products = []
for product in PLAID_PRODUCTS:
    products.append(Products(product))

access_token = None
item_id = None
transfer_id = None


class LinkController(MethodView):
    def __init__(self):
        self.logic = LinkLogic()

    @token_required
    def post(self, user_id):
        if request.path == '/api/create_link_token':
            return self.create_link_token()
        elif request.path == '/api/set_access_token':
            return self.get_access_token()

    @token_required
    def get(self, user_id):
        if request.path == '/api/transactions':
            return self.get_transactions(user_id)
        elif request.path == '/api/items':
            return self.get_items(user_id)

    def create_link_token(self):
        try:
            request = LinkTokenCreateRequest(
                products=products,
                client_name="Plaid Quickstart",
                country_codes=list(
                    map(lambda x: CountryCode(x), PLAID_COUNTRY_CODES)),
                language='en',
                user=LinkTokenCreateRequestUser(
                    client_user_id=str(time.time())
                )
            )
            # if PLAID_REDIRECT_URI!=None:
            #     request['redirect_uri']=PLAID_REDIRECT_URI
            if Products('statements') in products:
                statements = LinkTokenCreateRequestStatements(
                    end_date=date.today(),
                    start_date=date.today()-timedelta(days=30)
                )
                request['statements'] = statements
        # create link token
            response = client.link_token_create(request)
            return jsonify(response.to_dict())
        except plaid.ApiException as e:
            print(e)
            return json.loads(e.body)

    def get_access_token(self):
        try:
            public_token = request.json.get('public_token')
            user_id = AuthUtils.decode_request_auth(request=request)
            exchange_request = {'public_token': public_token}

            exchange_response = client.item_public_token_exchange(
                exchange_request)
            access_token = exchange_response['access_token']
            item_id = exchange_response['item_id']
            self.logic.store_plaid_link(
                user_id, access_token, item_id, None, None)
            return jsonify(exchange_response.to_dict())
        except plaid.ApiException as e:
            return json.loads(e.body)

    def get_transactions(self, user_id):
        transactions, error = self.logic.get_transactions(user_id)

        if error:
            return jsonify({
                'data': transactions,
            }), 400

        return jsonify({'data': transactions}), 200

    def get_items(self, user_id):
        res, error = self.logic.get_item(user_id=user_id)
        if error:
            return jsonify({'error': error}), 400
        return jsonify({'data': res}), 200


def pretty_print_response(response):
    print(json.dumps(response, indent=2, sort_keys=True, default=str))


def format_error(e):
    response = json.loads(e.body)
    return {'error': {'status_code': e.status, 'display_message':
                      response['error_message'], 'error_code': response['error_code'], 'error_type': response['error_type']}}


link_blueprint = Blueprint('link', __name__)

link_blueprint.add_url_rule(
    '/api/create_link_token', view_func=LinkController.as_view('create_link_token'), methods=['POST'])
link_blueprint.add_url_rule(
    '/api/set_access_token', view_func=LinkController.as_view('set_access_token'), methods=['POST'])
link_blueprint.add_url_rule(
    '/api/transactions', view_func=LinkController.as_view('transactions'), methods=['GET'])
link_blueprint.add_url_rule(
    '/api/items', view_func=LinkController.as_view('items'), methods=['GET'])
