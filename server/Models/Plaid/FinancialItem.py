from Models.SerializableModel import SerializableModel


class FinancialItem(SerializableModel):
    def __init__(self, item_id, webhook, error, available_products, billed_products, consent_expiration_time, update_type, institution_id, products):
        self.itemId = item_id
        self.id = item_id
        self.webhook = webhook
        self.error = error
        self.availableProducts = available_products
        self.billedProducts = billed_products
        self.consentExpirationTime = consent_expiration_time
        self.updateType = update_type
        self.institutionId = institution_id
        self.products = products

    def __init__(self, plaid_item):
        self.itemId = plaid_item.get('item_id')
        self.id = plaid_item.get('item_id')
        self.webhook = plaid_item.get('webhook')
        self.error = plaid_item.get('error')
        self.availableProducts = plaid_item.get('available_products')
        self.billedProducts = plaid_item.get('billed_products')
        self.consentExpirationTime = plaid_item.get('consent_expiration_time')
        self.updateType = plaid_item.get('update_type')
        self.institutionId = plaid_item.get('institution_id')
        self.products = plaid_item.get('products')
