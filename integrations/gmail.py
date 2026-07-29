"""
integrations/gmail.py
Gmail Integration using Google API Python Client
Requires: google-auth, google-auth-oauthlib, google-api-python-client
"""

import os
import base64
from email.mime.text import MIMEText


class GmailIntegration:
    def __init__(self):
        self.service = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Gmail using OAuth2."""
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build

            SCOPES = [
                "https://www.googleapis.com/auth/gmail.readonly",
                "https://www.googleapis.com/auth/gmail.send"
            ]

            creds = None
            token_path = "token.json"
            creds_path = "credentials.json"

            if os.path.exists(token_path):
                creds = Credentials.from_authorized_user_file(token_path, SCOPES)

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if not os.path.exists(creds_path):
                        print("[Gmail] credentials.json not found.")
                        return
                    flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                    creds = flow.run_local_server(port=0)

                with open(token_path, "w") as token:
                    token.write(creds.to_json())

            self.service = build("gmail", "v1", credentials=creds)
            print("[Gmail] Authenticated successfully.")

        except Exception as e:
            print(f"[Gmail] Auth failed: {e}")

    # ---------------- READ EMAILS ----------------
    def read_emails(self, n: int = 5) -> str:
        """Read latest N emails from inbox."""
        if not self.service:
            return "Gmail not configured. Please add credentials.json."

        try:
            results = self.service.users().messages().list(
                userId="me",
                labelIds=["INBOX"],
                maxResults=n
            ).execute()

            messages = results.get("messages", [])
            if not messages:
                return "No emails found in inbox."

            email_summaries = []

            for msg in messages:
                msg_data = self.service.users().messages().get(
                    userId="me",
                    id=msg["id"],
                    format="full"
                ).execute()

                # ---------- headers ----------
                headers = {
                    h["name"]: h["value"]
                    for h in msg_data["payload"]["headers"]
                }

                # ---------- body ----------
                body = ""

                payload = msg_data.get("payload", {})

                if "parts" in payload:
                    for part in payload["parts"]:
                        if part.get("mimeType") == "text/plain":
                            data = part["body"].get("data")
                            if data:
                                body = base64.urlsafe_b64decode(
                                    data.encode("UTF-8")
                                ).decode("utf-8", errors="ignore")
                                break
                else:
                    data = payload.get("body", {}).get("data")
                    if data:
                        body = base64.urlsafe_b64decode(
                            data.encode("UTF-8")
                        ).decode("utf-8", errors="ignore")

                # ---------- summary ----------
                email_summaries.append(
                    f"From: {headers.get('From', 'Unknown')}\n"
                    f"Subject: {headers.get('Subject', 'No Subject')}\n"
                    f"Date: {headers.get('Date', 'Unknown')}\n\n"
                    f"Body:\n{body[:500]}"
                )

            return "\n\n---\n\n".join(email_summaries)

        except Exception as e:
            return f"Failed to read emails: {str(e)}"

    # ---------------- SEND EMAIL ----------------
    def send_email(self, to: str, subject: str, body: str) -> str:
        """Send an email."""
        if not self.service:
            return "Gmail not configured. Please add credentials.json."

        try:
            message = MIMEText(body)
            message["to"] = to
            message["subject"] = subject

            raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

            self.service.users().messages().send(
                userId="me",
                body={"raw": raw}
            ).execute()

            return f"Email sent to {to} with subject '{subject}'."

        except Exception as e:
            return f"Failed to send email: {str(e)}"