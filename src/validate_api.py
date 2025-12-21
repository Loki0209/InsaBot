"""
API Key Validation Module
Validates all required API keys before running the bot
"""

import os
import sys
from typing import Dict, List, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def validate_api_keys() -> Tuple[bool, List[str]]:
    """
    Validate all required API keys are present and properly formatted.

    Returns:
        Tuple[bool, List[str]]: (is_valid, list_of_error_messages)
    """

    errors = []
    warnings = []

    print("=" * 70)
    print(" " * 20 + "API KEY VALIDATION")
    print("=" * 70)
    print()

    # Required API Keys
    required_keys = {
        "NEWSAPI_KEY": {
            "name": "NewsAPI",
            "url": "https://newsapi.org/register",
            "format": "32 characters",
            "example": "6d388bfb6ca74ee1afccaad89c665920"
        },
        "GEMINI_API_KEY": {
            "name": "Google Gemini API",
            "url": "https://aistudio.google.com/app/apikey",
            "format": "Starts with 'AIzaSy'",
            "example": "AIzaSyD-xxxxxxxxxxxxxxxxxxxxxxx"
        }
    }

    # Optional API Keys
    optional_keys = {
        "EDGE_TTS_VOICE": {
            "name": "EdgeTTS Voice (Optional)",
            "url": "https://github.com/rany2/edge-tts",
            "info": "FREE! Default: en-US-AriaNeural. List all: python list_voices.py"
        },
        "PEXELS_API_KEY": {
            "name": "Pexels API (Optional)",
            "url": "https://www.pexels.com/api/",
            "info": "For real stock photos instead of gradients"
        }
    }

    # Validate required keys
    print("Checking Required API Keys:")
    print("-" * 70)

    for key_name, key_info in required_keys.items():
        key_value = os.getenv(key_name, "").strip()

        if not key_value or key_value.startswith("your_"):
            errors.append(
                f"[X] {key_info['name']} ({key_name}) is missing!\n"
                f"  Get it from: {key_info['url']}\n"
                f"  Format: {key_info['format']}\n"
                f"  Example: {key_info['example']}"
            )
            print(f"[X] {key_info['name']:30} NOT CONFIGURED")
        else:
            # Basic format validation
            if key_name == "NEWSAPI_KEY" and len(key_value) != 32:
                warnings.append(
                    f"[!] {key_info['name']} format looks incorrect (expected 32 chars, got {len(key_value)})"
                )
                print(f"[!] {key_info['name']:30} CONFIGURED (format warning)")
            elif key_name == "GEMINI_API_KEY" and not key_value.startswith("AIzaSy"):
                warnings.append(
                    f"[!] {key_info['name']} format looks incorrect (should start with 'AIzaSy')"
                )
                print(f"[!] {key_info['name']:30} CONFIGURED (format warning)")
            else:
                print(f"[OK] {key_info['name']:30} CONFIGURED")

    print()

    # Check optional keys
    print("Checking Optional API Keys:")
    print("-" * 70)

    for key_name, key_info in optional_keys.items():
        key_value = os.getenv(key_name, "").strip()

        if not key_value or key_value.startswith("your_"):
            print(f"[ ] {key_info['name']:30} NOT SET (will use fallback)")
        else:
            print(f"[OK] {key_info['name']:30} CONFIGURED")

    print()
    print("=" * 70)

    # Display errors if any
    if errors:
        print()
        print("[FAILED] VALIDATION FAILED - Missing Required API Keys:")
        print("=" * 70)
        for error in errors:
            print(error)
            print()

        print("=" * 70)
        print("QUICK FIX:")
        print("=" * 70)
        print("1. Open the .env file in the project root")
        print("2. Add your API keys (remove 'your_' placeholders)")
        print("3. Save the file and run the bot again")
        print()
        print("Need help? Check README.md for detailed setup instructions!")
        print("=" * 70)
        return False, errors

    # Display warnings if any
    if warnings:
        print()
        print("[WARNING] API Keys May Be Incorrect:")
        print("=" * 70)
        for warning in warnings:
            print(warning)
        print()
        print("Bot will attempt to run, but may fail if keys are invalid.")
        print("=" * 70)

    print()
    print("[SUCCESS] ALL REQUIRED API KEYS VALIDATED!")
    print("=" * 70)
    print()

    return True, []


if __name__ == "__main__":
    """
    Test the API key validation
    """
    is_valid, errors = validate_api_keys()

    if not is_valid:
        print("\n[FAILED] Validation failed!")
        sys.exit(1)
    else:
        print("[SUCCESS] All API keys are properly configured!")
        print("Ready to run: python main.py")
