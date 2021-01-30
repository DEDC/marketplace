import stripe

stripe.api_key = "sk_test_51I7T2kE4OKuuVvsDk8L6AodX0LfALn6k4IvE52tdKvSPlWDohb1BgwmQBZOOjIleZOyrPlC4uCCMoGbGSFbxVkpp00lfgh18e2"

# Token is created using Stripe Checkout or Elements!
# Get the payment token ID submitted by the form:
token = request.form['stripeToken'] # Using Flask

charge = stripe.Charge.create(
  amount=999,
  currency='usd',
  description='Example charge',
  source=token,
)