var stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
//var stripe = Stripe(stripe_public_key);
// Create a Stripe client.
//alert(stripe_public_key);
//var stripe = Stripe('pk_test_IsjjZmU79vK4VvuALK5XgACe');
var stripe = Stripe(stripe_public_key);

// Create an instance of Elements.
var elements = stripe.elements();

// Custom styling can be passed to options when creating an Element.
// (Note that this demo uses a wider set of styles than the guide below.)
var style = {
  base: {
    color: '#32325d',
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: 'antialiased',
    fontSize: '16px',
    '::placeholder': {
      color: '#aab7c4'
    }
  },
  invalid: {
    color: '#fa755a',
    iconColor: '#fa755a'
  }
};

// Create an instance of the card Element.
var card = elements.create('card', {hidePostalCode: true,style: style});

// Add an instance of the card Element into the `card-element` <div>.
card.mount('#card-element');

// Handle real-time validation errors from the card Element.
card.on('change', function(event) {
  var displayError = document.getElementById('card-errors');
  if (event.error) {
    //displayError.textContent = event.error.message;
    var html = `
    <span class="alert alert-danger mt-2 d-block"><i class="fa fa-times"> ${event.error.message}</i></span>
    `;
    $(displayError).html(html);
  } else {
    displayError.textContent = '';
  }
});

// Handle form submission.
// var form = document.getElementById('payment-form');
// form.addEventListener('submit', function(event) {
//   event.preventDefault();
//   card.update({'disabled': true});
//   $('#submit-button').attr('disabled', true);
//   stripe.createToken(card).then(function(result) {
//     if (result.error) {
//       // Inform the user if there was an error.
//       var errorElement = document.getElementById('card-errors');
//       var html = `
//       <span class="alert alert-danger mt-2 d-block"><i class="fa fa-times"> ${event.error.message}</i></span>
//       `;
//       $(errorElement).html(html);
//       //errorElement.textContent = result.error.message;
//         card.update({'disabled': false});
//         $('#submit-button').attr('disabled', false);
//     } else {
//       // Send the token to your server.
//       stripeTokenHandler(result.token);
//     }
//   });
// });
//
// // Submit the form with the token ID.
// function stripeTokenHandler(token) {
//   // Insert the token ID into the form so it gets submitted to the server
//   var form = document.getElementById('payment-form');
//   var hiddenInput = document.createElement('input');
//   hiddenInput.setAttribute('type', 'hidden');
//   hiddenInput.setAttribute('name', 'stripeToken');
//   hiddenInput.setAttribute('value', token.id);
//   form.appendChild(hiddenInput);
//
//   // Submit the form
//   form.submit();
// }

var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
  ev.preventDefault();
  card.update({'disabled': true});
  $('#submit-button').attr('disabled', true);
  stripe.confirmCardPayment(clientSecret, {
    payment_method: {
      card: card,
    }
  }).then(function(result) {
    if (result.error) {
      // Show error to your customer (e.g., insufficient funds)
      var displayError = document.getElementById('card-errors');
      var html = `
      <span class="alert alert-danger mt-2 d-block"><i class="fa fa-times"> ${event.error.message}</i></span>
      `;
      $(displayError).html(html);
      card.update({'disabled': false});
      $('#submit-button').attr('disabled', false);
    } else {
      // The payment has been processed!
      if (result.paymentIntent.status === 'succeeded') {
        form.submit();
      }
    }
  });
});
