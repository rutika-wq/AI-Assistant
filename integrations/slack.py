"""
integrations/slack.py
Slack Integration using Slack SDK
Requires: slack-sdk
"""

import os


class SlackIntegration:
    def __init__(self):
        self.client = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Slack using Bot Token."""
        try:
            from slack_sdk import WebClient
            token = os.getenv("SLACK_BOT_TOKEN")
            if not token:
                print("[Slack] SLACK_BOT_TOKEN not found in .env. Slack features disabled.")
                return
            self.client = WebClient(token=token)
            print("[Slack] Authenticated successfully.")
        except ImportError:
            print("[Slack] slack-sdk not installed. Run: pip install slack-sdk")
        except Exception as e:
            print(f"[Slack] Auth failed: {e}")

    def send_message(self, channel: str, message: str) -> str:
        """Send a message to a Slack channel."""
        if not self.client:
            return "Slack not configured. Please add SLACK_BOT_TOKEN to .env."
        try:
            # Add # if not present
            if not channel.startswith("#"):
                channel = f"#{channel}"
            result = self.client.chat_postMessage(channel=channel, text=message)
            return f"Message sent to {channel}."
        except Exception as e:
            return f"Failed to send Slack message: {str(e)}"

    def read_channel(self, channel: str, limit: int = 5) -> str:
        """Read recent messages from a Slack channel."""
        if not self.client:
            return "Slack not configured. Please add SLACK_BOT_TOKEN to .env."
        try:
            if not channel.startswith("#"):
                channel = f"#{channel}"

            # First, find the channel ID
            channels_list = self.client.conversations_list()
            channel_id = None
            for ch in channels_list["channels"]:
                if ch["name"] == channel.lstrip("#"):
                    channel_id = ch["id"]
                    break

            if not channel_id:
                return f"Channel {channel} not found."

            result = self.client.conversations_history(channel=channel_id, limit=limit)
            messages = result.get("messages", [])

            if not messages:
                return f"No messages found in {channel}."

            summaries = []
            for msg in messages:
                user = msg.get("user", "Unknown")
                text = msg.get("text", "")
                summaries.append(f"[{user}]: {text}")

            return "\n".join(summaries)
        except Exception as e:
            return f"Failed to read Slack channel: {str(e)}"
