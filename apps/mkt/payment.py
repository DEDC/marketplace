import openpay
import json
import decimal

openpay.api_key = "sk_8667200e83e842b5a104f0415f079df2"
openpay.verify_ssl_certs = False
openpay.merchant_id = "mpelhavr5dmqvjndxovd"
openpay.production = False


class PaymentOPP():
    def __init__(self, customer = None):
        self.customer = customer

    def create_customer(self, name, last_name, email, phone_number):
        custosmer = openpay.Customer.create(
            name = name,
            last_name = last_name,
            email = email,
            phone_number = phone_number
        )
        self.customer = custosmer
        return custosmer

    def customer_charge(self, token, device_session, amount = 0, description = 'Cargo de Marketplace'):
        charge = self.customer.charges.create(
            source_id = token,
            method = 'card',
            amount =  str(amount),
            description = description,
            capture = True,
            device_session_id = device_session
        )
        return charge