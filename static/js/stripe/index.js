'use strict'

var stripe = Stripe('pk_live_51I7T2kE4OKuuVvsDF4talTmj4SYyhYfulAJvPsknmlHvDKqcBMxdrVlVsErxqYUx09qRCOQ0CWwUmB2NLa9ZSXGR00AQRGb5Tt')
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
}

var card = elements.create('card', { style: style })
var card_name = document.querySelector('#cardname')
var cont_payment = document.querySelector('#cont-payment')
const form = document.getElementById('payment-form')
var selected_card = document.querySelector('#card')
var add_method = document.querySelector('#add_method')
var remove_method = document.querySelector('#remove_method')
var btn = form.querySelector('#btn-pay')
var progress = document.querySelector('.progress')
progress.style.display = 'none'

if (!selected_card.value) {
  card.mount('#card-element')
}
else {
  cont_payment.style.display = 'none'
  card_name.required = false
}

form.addEventListener('submit', function (event) {
  event.preventDefault()
  let card_element = document.querySelector('#card-element')
  if (card_element) {
    if (card_element.classList.contains('StripeElement')) {
      stripe.createToken(card, { name: card_name.value }).then(function (result) {
        if (result.error) {
          var errorElement = document.getElementById('card-errors')
          errorElement.textContent = result.error.message
        } else {
          btn.disabled = true
          progress.style.display = 'block'
          stripeTokenHandler(result.token)
        }
      })
    }
    else if (selected_card.value) {
      btn.disabled = true
      progress.style.display = 'block'
      form.submit()
    }
  }
})

add_method.addEventListener('click', function (e) {
  e.preventDefault()
  card.mount('#card-element')
  cont_payment.style.display = 'block'
  card_name.required = true
})

remove_method.addEventListener('click', function (e) {
  e.preventDefault()
  card.unmount()
  cont_payment.style.display = 'none'
  card_name.required = false
})

function stripeTokenHandler(token) {
  var hiddenInput = document.createElement('input')
  hiddenInput.setAttribute('type', 'hidden')
  hiddenInput.setAttribute('name', 'stripeToken')
  hiddenInput.setAttribute('value', token.id)
  form.appendChild(hiddenInput)
  form.submit()
}