import httpx
import random
from dotenv import load_dotenv
import os

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY" , "")
SENDER_EMAIL = os.getenv("SENDER_EMAIL" , "")

def generate_otp() -> str:
    return str(random.randint(1000, 9999))

async def send_otp_email(receiver_email: str, otp_code: str) -> bool:
    url = "https://api.brevo.com/v3/smtp/email"
    
    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }
    
    html_body = f"""
    <html>
        <body style="background-color: #0a0f1d; color: #e2e8f0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 40px 20px; text-align: center; margin: 0;">
            <div style="max-width: 480px; margin: 0 auto; background: #111827; border: 1px solid #1e40af; border-radius: 24px; padding: 35px 25px; box-shadow: 0 10px 25px -5px rgba(29, 78, 216, 0.3);">
                
                <h1 style="color: #3b82f6; margin-bottom: 5px; font-weight: 800; letter-spacing: 2px; font-size: 2rem;">STATION ✦</h1>
                <p style="color: #60a5fa; font-size: 0.85rem; margin-top: 0; font-weight: 500; letter-spacing: 1px;">iliiz AI Core Registration</p>
                
                <hr style="border: 0; height: 1px; background: linear-gradient(to right, transparent, #3b82f6, transparent); margin: 25px 0;">
                
                <p style="font-size: 1rem; color: #94a3b8; line-height: 1.6; margin-top: 10px;">
                    Thank you for creating an account. Use the secure activation code below to link your session with <strong style="color: #60a5fa;">iliiz AI</strong>:
                </p>
                
                <div style="background-color: rgba(30, 58, 138, 0.4); border: 1px solid #2563eb; display: inline-block; padding: 14px 40px; border-radius: 16px; font-size: 2.5rem; font-weight: 800; color: #60a5fa; letter-spacing: 8px; margin: 25px 0; font-family: 'Courier New', Courier, monospace; box-shadow: inset 0 0 10px rgba(59, 130, 246, 0.2);">
                    {otp_code}
                </div>
                
                <p style="color: #64748b; font-size: 0.75rem; margin-top: 25px; line-height: 1.4;">
                    This security token is strictly confidential, one-time use only, and will expire in <span style="color: #ef4444; font-weight: 600;">5 minutes</span>.
                </p>
                
            </div>
        </body>
    </html>
    """
    
    payload = {
        "sender": {"name": "iliiz AI Support", "email": SENDER_EMAIL},
        "to": [{"email": receiver_email}],
        "subject": "Verification Code - STATION ✦",
        "htmlContent": html_body
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            if response.status_code in [200, 201, 202]:
                print(f"[BREVO API] Security token successfully delivered to {receiver_email}")
                return True
            else:
                print(f"[BREVO ERROR] API Rejected request: {response.text}")
                return False
    except Exception as e:
        print(f"[EMAIL SYSTEM ERROR] Exception caught during transport: {e}")
        return False