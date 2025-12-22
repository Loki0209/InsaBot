"""
Instagram Login Test Script
Quick test to verify credentials and diagnose login issues
"""

import os
import sys
from dotenv import load_dotenv

# Load environment
load_dotenv()

try:
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, ChallengeRequired, PleaseWaitFewMinutes
except ImportError:
    print("[ERROR] Instagrapi not installed!")
    print("Run: pip install instagrapi")
    sys.exit(1)

def test_login():
    """Test Instagram login with current credentials."""

    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")

    if not username or not password:
        print("[ERROR] Instagram credentials not found in .env file!")
        return False

    print("=" * 60)
    print("INSTAGRAM LOGIN TEST")
    print("=" * 60)
    print(f"Username: {username}")
    print(f"Password: {'*' * len(password)}")
    print("=" * 60)

    print("\n[INFO] Creating Instagram client...")
    client = Client()

    # Set more realistic settings
    client.delay_range = [2, 5]

    print("[INFO] Attempting login...")
    print("[INFO] This may take 15-30 seconds...")

    try:
        # Try login
        client.login(username, password)

        # Get user info to verify
        user_id = client.user_id
        user_info = client.user_info(user_id)

        print("\n" + "=" * 60)
        print("[SUCCESS] LOGIN SUCCESSFUL!")
        print("=" * 60)
        print(f"User ID: {user_id}")
        print(f"Username: {user_info.username}")
        print(f"Full Name: {user_info.full_name}")
        print(f"Followers: {user_info.follower_count}")
        print(f"Following: {user_info.following_count}")
        print(f"Posts: {user_info.media_count}")
        print("=" * 60)

        # Save session
        session_file = "data/temp/test_session.json"
        os.makedirs(os.path.dirname(session_file), exist_ok=True)
        client.dump_settings(session_file)
        print(f"\n[INFO] Session saved to: {session_file}")

        return True

    except ChallengeRequired as e:
        print("\n" + "=" * 60)
        print("[ERROR] CHALLENGE REQUIRED!")
        print("=" * 60)
        print(f"Error: {e}")
        print("\nInstagram requires verification:")
        print("1. Open Instagram app on your phone")
        print("2. Login with your account")
        print("3. Complete the challenge (CAPTCHA, 2FA, etc.)")
        print("4. Wait 10 minutes")
        print("5. Try this test again")
        return False

    except PleaseWaitFewMinutes as e:
        print("\n" + "=" * 60)
        print("[ERROR] RATE LIMITED!")
        print("=" * 60)
        print(f"Error: {e}")
        print("\nInstagram has blocked login attempts temporarily.")
        print("Wait 30-60 minutes and try again.")
        return False

    except Exception as e:
        error_msg = str(e)
        print("\n" + "=" * 60)
        print("[ERROR] LOGIN FAILED!")
        print("=" * 60)
        print(f"Error: {error_msg}")

        if "password" in error_msg.lower() or "incorrect" in error_msg.lower():
            print("\nPOSSIBLE ISSUES:")
            print("1. Password is incorrect")
            print("2. Account has 2FA enabled (disable it)")
            print("3. IP is blocked by Instagram")
            print("\nVERIFY:")
            print("- Try logging in at https://www.instagram.com")
            print("- If web login works, then IP is the issue")
            print("- If web login fails, password is wrong")

        elif "ip" in error_msg.lower() or "blacklist" in error_msg.lower():
            print("\nIP BLOCKED!")
            print("Your IP address is blacklisted by Instagram.")
            print("Solutions:")
            print("1. Wait 2-4 hours")
            print("2. Change network (mobile hotspot)")
            print("3. Use VPN")

        return False

if __name__ == "__main__":
    print("\nInstagram Login Test Tool")
    print("This will test if your credentials work\n")

    success = test_login()

    if success:
        print("\n[SUCCESS] Test passed! Your bot should work now.")
        print("Run: python main.py")
    else:
        print("\n[FAILED] Test failed! Fix the issues above before running bot.")

    sys.exit(0 if success else 1)
