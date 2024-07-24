import os
import plaid


class PlaidConfiguration:
    def __init__(self):
        self.client_id = os.getenv('PLAID_CLIENT_ID')
        self.secret = os.getenv('PLAID_SECRET')
        self.env = os.getenv('PLAID_ENV', 'sandbox')
        self.products = os.getenv('PLAID_PRODUCTS', 'transactions').split(',')
        self.country_codes = os.getenv('PLAID_COUNTRY_CODES', 'US').split(',')

        if self.env == 'sandbox':
            self.host = plaid.Environment.Sandbox
        elif self.env == 'development':
            self.host = plaid.Environment.Development
        elif self.env == 'production':
            self.host = plaid.Environment.Production
        else:
            raise ValueError("Invalid PLAID_ENV value")

        self.configuration = plaid.Configuration(
            host=self.host,
            api_key={
                'clientId': self.client_id,
                'secret': self.secret,
                'plaidVersion': '2020-09-14'
            }
        )

    def get_configuration(self):
        return self.configuration

    def get_country_codes(self):
        return self.country_codes
