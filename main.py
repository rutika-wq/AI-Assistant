"""
AI Personal Assistant - Main Entry Point
Powered by Gemini
"""

import os
import certifi

# Fix SSL certificate path for PyInstaller executable
os.environ["SSL_CERT_FILE"] = certifi.where()

from dotenv import load_dotenv
from assistant import AIAssistant
from ui.app import launch_ui

load_dotenv()


def main():
    print("=" * 50)
    print("  AI Personal Assistant - Powered by Gemini")
    print("=" * 50)

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        print("[ERROR] GROQ_API_KEY not found in .env file.")
        print("Please add your key to the .env file and try again.")
        input("Press Enter to exit...")
        return

    try:
        assistant = AIAssistant(api_key=api_key)
        launch_ui(assistant)

    except Exception as e:
        print("\n[ERROR]")
        print(e)
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()