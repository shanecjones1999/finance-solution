from Models.SerializableModel import SerializableModel


class FinancialInstitution(SerializableModel):
    def __init__(self, institution_id, name, products, country_codes, routing_numbers, oauth, dtc_numbers):
        self.institutionId = institution_id
        self.id = institution_id
        self.name = name
        self.products = products
        self.countryCodes = country_codes
        self.routingNumbers = routing_numbers
        self.oauth = oauth
        self.dtcNumbers = dtc_numbers

    def __init__(self, plaid_institution):
        self.institutionId = plaid_institution['institution_id']
        self.id = plaid_institution['institution_id']
        self.name = plaid_institution['name']
        self.products = plaid_institution['products']
        self.countryCodes = plaid_institution['country_codes']
        self.routingNumbers = plaid_institution['routing_numbers']
        self.oauth = plaid_institution['oauth']
        self.dtcNumbers = plaid_institution['dtc_numbers']
