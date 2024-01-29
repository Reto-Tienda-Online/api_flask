
import json
import os
import stripe

from flask import Flask, jsonify, request


stripe.api_key = "sk_test_..."

endpoint_secret = 'whsec_123'

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)