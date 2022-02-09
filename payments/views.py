from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
import json
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.log = 'info'  # or 'debug'

# How it works - in 3 steps:
# 1. GET TOKEN_ID, DESCRIPTION, CURRENCY, AMOUNT FROM FRONTEND
"""
#2.
try:
    stripe.Charge.create(
            amount is in cents: i.e 999 is 9.99
            amount      = request.POST.get('amount', ''),
            currency    = request.POST.get('currency', ''),
            source      = request.POST.get('source', ''), #token.id
            description = request.POST.get('description', '')
            statement_descriptor will appear in user's credit card statement
            statement_descriptor = "Company XYX",
            metadata={"order_id": 123456}
            )
            Statement descriptors are limited to 22 characters, cannot use the
            special characters <, >, ', or ", and must not consist solely of numbers.
            metadata is the opposite and will only appear in your DASHBOARD(e.g when
            looking at the page for an individual charge) and is also available in common
            reports and exports. As an example, your store's order ID can be attached to
            the charge used to pay for that order.
            (!!! DONT STORE ANY SENSITIVE INFORMATION - CARD DETAILS ETC as metadata or
            in the charge's description parameter)
"""
# 3 Return response to my frontend to display a confirmation / error

"""
- Optional: #2 can create a new model instance storing the customers_payment i.e
name, address of customer,
"""


@require_http_methods(['POST'])
@csrf_exempt
def checkout(request):

    post_data = json.loads(request.body)
    try:
        payment = stripe.PaymentIntent.create(
            amount=post_data.get('amount', ''),
            currency=post_data.get('currency', ''),
            payment_method=post_data.get('source', ''),
            payment_method_types=["card"],
            confirm=True,
            return_url="http://localhost:3000/home/order",
            metadata={
                'name': post_data.get('name'), 
                'email': post_data.get('email'), 
                'phone': post_data.get('phone'),
                'created': post_data.get('created_on')
            }
        )
        # Only confirm an order after you have status: succeeded
        if payment['status'] == 'succeeded':
            # PLACE ORDER LOGIC
            return HttpResponse(json.dumps(
                {'message': 'Your transaction has been successful.', 'ok':True})
            )
        else:
            raise stripe.error.CardError
    except stripe.error.CardError as e:
        body = e.json_body
        err = body.get('error', {})
        print('Status is: %s' % e.http_status)
        print('Type is: %s' % err.get('type'))
        print('Code is: %s' % err.get('code'))
        print('Message is %s' % err.get('message'))
        # return HttpResponse(
        #     json.dumps({"message": err.get('message'), "ok":False}),
        #     status=e.http_status
        # )
        return HttpResponse(
            json.dumps({"message": err.get('message'), "ok":False})
        )
    except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
        return HttpResponse(json.dumps({
            'message': "The API was not able to respond, try again.", 'ok':False
        }))
    except stripe.error.InvalidRequestError as e:
        # invalid parameters were supplied to Stripe's API
        return HttpResponse(json.dumps({
            'message': "Invalid parameters, unable to process payment.", 'ok':False
        }))
    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        pass
    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        return HttpResponse(json.dumps({
            'message': 'Network communication failed, try again.', 'ok':False
        }))
    except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe
        # send yourself an email
        return HttpResponse(json.dumps({
            'message': 'Internal Error, contact support.', 'ok':False
        }))

    # Something else happened, completely unrelated to Stripe
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({
            'message': 'Unable to process payment, try again.', 'ok':False
        }))
