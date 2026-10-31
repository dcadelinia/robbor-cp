import sqlite3
import os 

DB_FILE = "mantagu_users.db" 

def init_db():
"""Initializes the database schema for users and billing states."""
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
user_id TEXT PRIMARY KEY,
email TEXT NOT NULL,
tier TEXT DEFAULT 'Hobby',
status TEXT DEFAULT 'inactive',
frames_consumed INTEGER DEFAULT 0,
stripe_customer_id TEXT
)
""")
conn.commit()
conn.close() 

def update_user_subscription(user_id, email, tier, status, customer_id):
"""Inserts or updates user subscription lifecycle records."""
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute("""
INSERT INTO users (user_id, email, tier, status, stripe_customer_id, frames_consumed)
VALUES (?, ?, ?, ?, ?, 0)
ON CONFLICT(user_id) DO UPDATE SET
tier=excluded.tier,
status=excluded.status,
stripe_customer_id=excluded.stripe_customer_id
""", (user_id, email, tier, status, customer_id))
conn.commit()
conn.close() 

def get_user_data(user_id):
"""Retrieves user telemetry caps and active subscription tier profiles."""
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute("SELECT user_id, email, tier, status, frames_consumed FROM users WHERE user_id = ?", (user_id,))
row = cursor.fetchone()
conn.close()
if row:
return {"user_id": row, "email": row, "tier": row, "status": row, "frames_consumed": row}
return None 

### Self-initialize schema on import context

init_db()
