# Python
from decimal import Decimal
# Django
from django.contrib import messages
# Stripe
import stripe
# app payment
from .models import Customers
# app utils
from utils.models.operations import get_percent, get_iva

stripe.api_key = "sk_test_51I7T2kE4OKuuVvsDk8L6AodX0LfALn6k4IvE52tdKvSPlWDohb1BgwmQBZOOjIleZOyrPlC4uCCMoGbGSFbxVkpp00lfgh18e2"
stripe_raise_errors = (stripe.error.APIConnectionError, stripe.error.APIError, stripe.error.AuthenticationError, stripe.error.CardError, stripe.error.IdempotencyError, stripe.error.InvalidRequestError, stripe.error.RateLimitError, stripe.error.StripeError)

class PaymentStripe():
    def __init__(self, user):
        self.user = user
        self.customer, self.local_customer = self.get_or_create_customer()

    def make_charge(self, amount, token, invoice, request, customer = None):
        try:
            if customer is not None:
                charge = stripe.Charge.create(
                    amount = amount,
                    currency = 'mxn',
                    description = f'Cargo de compra en compratabasco.com con folio {invoice}',
                    source = token,
                    customer = customer
                )
            else:
                charge = stripe.Charge.create(
                    amount = amount,
                    currency = 'mxn',
                    description = f'Cargo de compra en compratabasco.com con folio {invoice}',
                    source = token
                )
            return charge
        except stripe.error.CardError as e:
            messages.error(request, 'La tarjeta fue declinada')
            # print('Status is: %s' % e.http_status)
            # print('Code is: %s' % e.code)
            # param is '' in this case
            # print('Param is: %s' % e.param)
            # print('Message is: %s' % e.user_message)

        except stripe_raise_errors as e:
            print(e)
            pass
        except Exception as e:
            print(e)
            pass
        return None
    
    def create_customer(self, local_create = True, remote_create = True):
        customer = None
        local_customer = None
        try:
            if remote_create:
                customer = stripe.Customer.create(
                    email = self.user.email,
                    name = self.user.get_full_name(),
                    phone = self.user.phone_number,
                )
            if local_create:
                local_customer = Customers.objects.create(user = self.user, id_customer = (customer['id'] if hasattr(customer, 'id') else self.customer['id']))
        except stripe_raise_errors as e:
            pass
        except Exception as e:
            pass
        return (customer, local_customer)
            
    def get_customer(self):
        customer = None
        local_customer = None
        try:
            local_customer = Customers.objects.get(user = self.user)
            customer = stripe.Customer.retrieve(local_customer.id_customer)
        except Customers.DoesNotExist:
            pass
        except stripe_raise_errors as e:
            pass
        except Exception as e:
            pass
        return (customer, local_customer)

    def get_or_create_customer(self):
        customer, local_customer = self.get_customer()
        if customer is not None and local_customer is not None:
            return (customer, local_customer)
        else:
            if customer is None and local_customer is not None:
                customer = self.create_customer(local_create = False)[0]
                local_customer.id_customer = customer['id']
                local_customer.save()
            elif customer is not None and local_customer is None:
                local_customer = self.create_customer(remote_create = False)[1]
            elif customer is None and local_customer is None:
                customer, local_customer = self.create_customer()
            else:
                pass
                #log al fallar get_or_create_customer
            return (customer, local_customer)
    
    def add_customer_card(self, token):
        card = None
        try:
            card = stripe.Customer.create_source(
                self.customer['id'],
                source = token
            )
        except stripe_raise_errors as e:
            print(e)
        except Exception as e:
            print(e)
        return card
    
    def get_customer_cards(self):
        card_list = []
        customer = self.customer
        if customer is not None:
            try:
                cards = stripe.Customer.list_sources(customer['id'])
                for card in cards:
                    card_list.append(
                        {
                            'id': card['id'],
                            'brand': card['brand'],
                            'last4': card['last4'],
                            'exp_month': card['exp_month'],
                            'exp_year': card['exp_year'],
                            'name': card['name']
                        }
                    )
            except stripe_raise_errors as e:
                pass
            except Exception as e:
                pass
        return card_list
    
    def customer_card_exists(self, card_id):
        try:
            customer = self.customer
            card = stripe.Customer.retrieve_source(customer['id'], card_id)
            return True
        except stripe_raise_errors as e:
            return False
    
    def stripe_cost(self, amount):
        stripe_trans = Decimal(3.6)
        stripe_cost = 3
        stripe_total = get_percent(amount, stripe_trans) + stripe_cost
        return round(get_iva(stripe_total) + stripe_total, 2)

class SimpleStripe(PaymentStripe):
    def __init__(self, user):
        super(SimpleStripe).__init__()
        self.user = user
        self.customer, self.local_customer = self.get_customer()