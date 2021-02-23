'use strict';

var stripe = Stripe('pk_test_51I7T2kE4OKuuVvsDzt6ZZA4jnOq18zmAKFsNh7p3zJ8qAOoPPppvnPOGXQcfGBHCLoxupyKCsWg6flBeKFXreuHD00vOFme0XO')
var elements = stripe.elements()
var style = {
  base: {
    color: '#32325d',
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: 'antialiased',
    fontSize: '16px',
    '::placeholder': {
      color: '#616161'
    }
  },
  invalid: {
    color: '#fa755a',
    iconColor: '#fa755a'
  }
};
var card = elements.create('card', { style: style })
card.mount('#card-element')
var form = document.getElementById('payment-form');
form.addEventListener('submit', function (event) {
  event.preventDefault();
  let card_name = form.querySelector('#cardname')
  stripe.createToken(card, { name: card_name.value }).then(function (result) {
    if (result.error) {
      var errorElement = document.getElementById('card-errors');
      errorElement.textContent = result.error.message;
    } else {
      stripeTokenHandler(result.token);
    }
  });
});
function stripeTokenHandler(token) {
  var form = document.getElementById('payment-form');
  var hiddenInput = document.createElement('input');
  hiddenInput.setAttribute('type', 'hidden');
  hiddenInput.setAttribute('name', 'stripeToken');
  hiddenInput.setAttribute('value', token.id);
  form.appendChild(hiddenInput);
  form.submit();
}