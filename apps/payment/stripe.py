# Stripe
import stripe
# app payment
from .models import Customers

stripe.api_key = "sk_test_51I7T2kE4OKuuVvsDk8L6AodX0LfALn6k4IvE52tdKvSPlWDohb1BgwmQBZOOjIleZOyrPlC4uCCMoGbGSFbxVkpp00lfgh18e2"

class PaymentStripe():
    def __init__(self, user, initialize_customer = True):
        self.user = user
        if initialize_customer:
            self.customer, self.local_customer = self.get_or_create_customer()

    def make_charge(self, amount, token, invoice, customer = None):
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
                source = token,
            )
        return charge
    
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
        except (
            stripe.error.RateLimitError,
            stripe.error.InvalidRequestError,
            stripe.error.AuthenticationError,
            stripe.error.APIConnectionError,
            stripe.error.StripeError) as e:
            print(e)
            # log al fallar create_customer
        except Exception as e:
            print(e)
            # log al fallar create_customer
        return (customer, local_customer)
            
    
    def get_customer(self):
        customer = None
        local_customer = None
        try:
            local_customer = Customers.objects.get(user = self.user)
            customer = stripe.Customer.retrieve(local_customer.id_customer)
        except Customers.DoesNotExist:
            pass
            # log al fallar get_customer
        except (
            stripe.error.RateLimitError,
            stripe.error.InvalidRequestError,
            stripe.error.AuthenticationError,
            stripe.error.APIConnectionError,
            stripe.error.StripeError) as e:
            print(e)
            # log al fallar get_customer
        except Exception as e:
            print(e)
            # log al fallar get_customer
        return (customer, local_customer)

    def get_or_create_customer(self):
        print('holiiiiii')
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

        except (
            stripe.error.RateLimitError,
            stripe.error.InvalidRequestError,
            stripe.error.AuthenticationError,
            stripe.error.APIConnectionError,
            stripe.error.StripeError,
            stripe.error.CardError) as e:
            print(e)
            # log al fallar get_customer
        except Exception as e:
            print(e)
            # log al fallar get_customer
        return card
    
    def get_customer_cards(self, user):
        card_list = []
        customer = self.get_customer()[0]
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
            except (
                stripe.error.RateLimitError,
                stripe.error.InvalidRequestError,
                stripe.error.AuthenticationError,
                stripe.error.APIConnectionError,
                stripe.error.StripeError) as e:
                print(e)
                # log al fallar create_customer
            except Exception as e:
                print(e)
                # log al fallar create_customer
        return card_list