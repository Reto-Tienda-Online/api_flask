from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models.models import Resena, get_db, Usuario, Producto
from sqlalchemy import Text, text

stripe_bp = APIRouter()

from fastapi import FastAPI, HTTPException
import stripe

stripe.api_key = "sk_test_51ObKe0Icv58uqKJmTnWvjSDYmfPG1mibuvqF9vZB1ShgDXYsJFq8ggHnfIBy4cAOgzeFnECFDtT0G9yJtbwqlYeH00rB5WOmI7"


@stripe_bp.post("/process-payment/")
async def process_payment(data: dict):
    amount = data.get("amount")
    currency = data.get("currency")
    token = data.get("token")

    if not all([amount, currency, token]):
        raise HTTPException(status_code=400, detail="Invalid request data")

    try:
        # Create a charge using the Stripe API
        charge = stripe.Charge.create(
            amount=amount,
            currency=currency,
            source=token,
            description="Payment for Game Groove Store",
        )

        
        return {"status": "success", "charge_id": charge.id}

    except stripe.error.CardError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=500, detail="Something went wrong. Please try again later.")