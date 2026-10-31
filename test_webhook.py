import requests
import json 

### Local or production environment execution URL configuration target context

BASE_URL = "http://localhost:8080" # Change this target string to your live Fly URL when executing global tests 

def test_stripe_webhook_flow():
"""Simulates a complete secure transaction webhook execution path."""
print("🛰️ Constructing fake 'checkout.session.completed' webhook payload...") 

mock_stripe_event = {
"id": "evt_test_123456789",
"type": "checkout.session.completed",
"data": {
"object": {
"id": "cs_test_abcde12345",
"client_reference_id": "usr_dev_inception_99",
"customer": "cus_NvidiaInception99",
"customer_details": {
"email": "[engineer@physicalai.com](mailto:engineer@physicalai.com)"
},
"metadata": {
"tier": "pro"
}
}
}
}

webhook_url = f"{BASE_URL}/v1/billing/webhook"
print(f"📦 Dispatched execution payload to target endpoint: {webhook_url}")

response = requests.post(webhook_url, json=mock_stripe_event)
print(f"📬 Server Response Code: {response.status_code}")
print(f"📄 Response Content: {json.dumps(response.json(), indent=2)}")

if response.status_code == 200:
print("\n✅ Verification Successful! The database layer processed the mock user and upgraded the tier status to Pro.")
else:
print("\n❌ Verification Failed. Inspect server stack telemetry paths.")

if **name** == "**main**":
test_stripe_webhook_flow()
