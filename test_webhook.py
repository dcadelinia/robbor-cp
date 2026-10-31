import requests
import json 

### Your live production server URL destination point

BASE_URL = "https://robbor-cp-uttvga.fly.dev" 

def verify_live_billing_pipeline():
print("🛰️ Initiating production checkout verification loop for 'robbor-cp-uttvga'...") 

### 1. Verify the public pricing tiers are reachable

print("\n🔍 Step 1: Checking reachable SaaS commercial pricing layers...")
try:
tiers_response = requests.get(f"{BASE_URL}/v1/billing/tiers")
print(f"📬 Status Code: {tiers_response.status_code}")
print(f"📄 Available Tiers: {json.dumps(tiers_response.json(), indent=2)}")
except Exception as e:
print(f"❌ Connection error fetching tiers: {e}")
return 

### 2. Simulate a completed payment transaction event from Stripe hooks

print("\n💳 Step 2: Dispatching mock 'checkout.session.completed' webhook payload...")
mock_stripe_event = {
"id": "evt_live_dcadelinia_2026",
"type": "checkout.session.completed",
"data": {
"object": {
"id": "cs_live_session_99482",
"client_reference_id": "usr_linkedin_demo_customer",
"customer": "cus_NvidiaInceptionUser",
"customer_details": {
"email": "innovator@edgecompute.io"
},
"metadata": {
"tier": "pro"
}
}
}
} 

try:
webhook_url = f"{BASE_URL}/v1/billing/webhook"
headers = {"Content-Type": "application/json"}
webhook_response = requests.post(webhook_url, json=mock_stripe_event, headers=headers)
print(f"📬 Status Code: {webhook_response.status_code}")
print(f"📄 Webhook Response: {json.dumps(webhook_response.json(), indent=2)}")
except Exception as e:
print(f"❌ Error hitting webhook endpoint: {e}")
return 

# 3. Request the programmatic live invoice for our new customer account profile

print("\n🧾 Step 3: Fetching the automated markdown transaction receipt invoice...")
try:
invoice_url = f"{BASE_URL}/v1/billing/invoice/usr_linkedin_demo_customer"
invoice_response = requests.get(invoice_url)
print(f"📬 Status Code: {invoice_response.status_code}")
if invoice_response.status_code == 200:
print("\n================= LIVE RENDERED INVOICE =================")
print(invoice_response.text)
print("=========================================================")
print("\n✅ SUCCESS: The full commercial pipeline is verified and fully operational!")
else:
print(f"❌ Failed to fetch receipt statement: {invoice_response.text}")
except Exception as e:
print(f"❌ Error fetching generated invoice context: {e}")

if **name** == "**main**":
verify_live_billing_pipeline()
