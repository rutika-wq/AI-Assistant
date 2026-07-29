"""
integrations/whatsapp.py
WhatsApp Integration via Twilio Sandbox
Requires: twilio
"""

import os


class WhatsAppIntegration:
    def __init__(self):
        self.client = None
        self.from_number = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Twilio for WhatsApp."""
        try:
            from twilio.rest import Client
            account_sid = os.getenv("TWILIO_ACCOUNT_SID")
            auth_token = os.getenv("TWILIO_AUTH_TOKEN")
            self.from_number = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")

            if not account_sid or not auth_token:
                print("[WhatsApp] TWILIO credentials not found in .env. WhatsApp features disabled.")
                return

            self.client = Client(account_sid, auth_token)
            print("[WhatsApp] Twilio client initialized successfully.")
        except ImportError:
            print("[WhatsApp] twilio not installed. Run: pip install twilio")
        except Exception as e:
            print(f"[WhatsApp] Auth failed: {e}")

    def send_message(self, to_number: str, message: str) -> str:
        """Send a WhatsApp message via Twilio Sandbox."""
        if not self.client:
            return "WhatsApp not configured. Please add Twilio credentials to .env."

        try:
            # Ensure number is in the right format
            if not to_number.startswith("whatsapp:"):
                to_number = f"whatsapp:{to_number}"

            result = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            return f"WhatsApp message sent. SID: {result.sid}"
        except Exception as e:
            return f"Failed to send WhatsApp message: {str(e)}"
