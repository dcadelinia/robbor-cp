import datetime 

def generate_markdown_invoice(user_id, email, tier, amount):
"""Generates a professional markdown transaction invoice log statement."""
invoice_id = f"INV-{int(datetime.datetime.utcnow().timestamp())}"
date_str = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC") 

invoice_template = f"""# INVOICE RECEIPT: ODYNEX AXIS LOGISTICS LLC
**Invoice ID:** {invoice_id}
**Date:** {date_str}
**Payment Status:** PAID (Stripe Processing via Sunrise Banks, N.A.) 

### Bill To:

* **User ID:** {user_id}
* **Customer Email:** {email}

### Transaction Breakdowns

Item DescriptionSubscription CycleTotal Amount (USD)
****ManTAGU Telemetry Pipeline ({tier.upper()} Tier)****
Monthly Recurring${amount:.2f}

### Financial Compliance Summary

* **Currency:** USD ($)
* **Subtotal:** ${amount:.2f}
* **Tax Rate:** 0.00%
* **Total Amount Paid:** ${amount:.2f}

*Thank you for partnering with Odynex Axis Logistics LLC. Your spatial intelligence microVM cluster allocation parameters have been updated automatically.*
"""
return invoice_template
