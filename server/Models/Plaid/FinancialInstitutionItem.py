from Models.SerializableModel import SerializableModel
from Models.Plaid.FinancialInstitution import FinancialInstitution
from Models.Plaid.FinancialItem import FinancialItem


class FinancialInstitutionItem(SerializableModel):
    def __init__(self, institution: FinancialInstitution, item: FinancialItem):
        self.institution = institution
        self.item = item
        self.id = item.id
