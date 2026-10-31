import os
from fastapi import APIRouter, Header, HTTPException, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import db 

router = APIRouter(prefix="/v1/billing", tags=["Billing Engine"]) 

PRICING_TIERS = {
"starter": {"name": "Starter Plan", "price_usd": 29.00, "limits": "50k frames/day"},
"pro": {"name": "Pro Plan", "price_usd": 89.00, "limits": "1M frames/day + Redis Cache"}
} 

class CheckoutRequest(BaseModel):
user_id: str
email: str
tier: str 

@router.get("/tiers")
async def get_billing_tiers():
return {"currency": "USD", "tiers": PRICING_TIERS} 

@router.post("/checkout")
async def create_checkout_session(payload: CheckoutRequest):
if payload.tier not in PRICING_TIERS:
raise HTTPException(status_code=400, detail="Invalid tier selection.") 

# Simulating secure payment link creation context

checkout_url = f"[https://checkout.stripe.com/pay/mock_session_{payload.tier}_{payload.user_id}](https://checkout.stripe.com/pay/mock_session_{payload.tier}_{payload.user_id})"
return {
"status": "success",
"checkout_url": checkout_url,
"amount": PRICING_TIERS[payload.tier]["price_usd"]
}

@router.post("/webhook")
async def stripe_webhook(payload: dict):
"""Processes Stripe event webhooks to mutate database state profiles.""" 

### In production, process event = stripe.Webhook.construct_event(...)

if payload.get("type") == "checkout.session.completed":
data = payload.get("data", {}).get("object", {})
user_id = data.get("client_reference_id", "unknown_user")
email = data.get("customer_details", {}).get("email", "client@example.com")
tier = data.get("metadata", {}).get("tier", "starter")
customer_id = data.get("customer", "cus_default") 

# Write state changes permanently to disk
db.update_user_subscription(user_id, email, tier, "active", customer_id)
return {"processed": True, "action": "subscription_activated"}

return {"processed": True, "action": "ignored"}

@router.get("/dashboard", response_class=HTMLResponse)
async def serve_dashboard():
"""Serves the interactive terminal subscriber checkout checkout panel UI."""
return """
 

"""
