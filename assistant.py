from groq import Groq
from integrations.gmail import GmailIntegration
from integrations.slack import SlackIntegration
from integrations.whatsapp import WhatsAppIntegration

SYSTEM_PROMPT = "You are a smart AI personal assistant."


class AIAssistant:

    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)

        self.history = []
        self.gmail = GmailIntegration()
        self.slack = SlackIntegration()
        self.whatsapp = WhatsAppIntegration()

    def chat(self, user_message: str) -> str:

        text = user_message.lower()

        # Gmail
        if "email" in text or "mail" in text:
            return self.gmail.read_emails(2)

        # Slack
        if "read slack" in text:
            return self.slack.read_channel("new-channel", 5)

        if "send slack" in text:
            return self.slack.send_message(
                "new-channel",
                "Hello from AI Assistant"
            )

        # WhatsApp
        if "send whatsapp" in text:
            return self.whatsapp.send_message(
                "+918970447920",
                "Hello from AI Assistant"
            )

        # Normal AI chat
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )

        return response.choices[0].message.content

    def reset(self):
        self.history = []
        return "Conversation reset."