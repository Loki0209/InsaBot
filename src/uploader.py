"""
Instagram Uploader Module

This module handles uploading Instagram Reels using Instagrapi.
It supports:
- Reel upload with caption and hashtags
- Session management (login/logout)
- Error handling and retry logic
- Upload history tracking

Author: AI News Reel Bot
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

try:
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, PleaseWaitFewMinutes, ChallengeRequired
except ImportError:
    print("[ERROR] Instagrapi not installed. Run: pip install instagrapi")
    sys.exit(1)


class InstagramUploader:
    """
    Instagram Uploader class for posting Reels automatically.

    Features:
    - Automatic login with session persistence
    - Reel upload with custom captions
    - Hashtag support
    - Upload history tracking
    - Error handling and retry logic
    """

    def __init__(self, username: str, password: str, session_file: str = "data/temp/instagram_session.json"):
        """
        Initialize Instagram uploader.

        Args:
            username: Instagram username
            password: Instagram password
            session_file: Path to session file for persistence
        """
        self.username = username
        self.password = password
        self.session_file = session_file
        self.client = Client()

        # Configure client settings for better Instagram compatibility
        self.client.delay_range = [1, 3]  # Random delay between requests (1-3 seconds)

        # Set user agent to mimic real Instagram app
        self.client.set_user_agent("Instagram 269.0.0.18.75 Android (26/8.0.0; 480dpi; 1080x1920; Xiaomi; Mi 5s; capricorn; qcom; en_US; 314665256)")

        # Disable challenge resolver initially (can cause issues)
        # self.client.challenge_code_handler = None

        print(f"[INFO] Instagram Uploader initialized for: @{username}")

    def login(self) -> bool:
        """
        Login to Instagram with session persistence.
        FIXED: Proper session reuse without re-authentication

        Returns:
            True if login successful, False otherwise
        """
        import time

        try:
            # Try to load existing session (WITHOUT re-logging in)
            if os.path.exists(self.session_file):
                print("[INFO] Found existing Instagram session...")
                try:
                    self.client.load_settings(self.session_file)

                    # Verify session is valid WITHOUT calling login()
                    # This is the KEY FIX - don't re-authenticate if session works
                    print("[INFO] Validating session...")
                    self.client.get_timeline_feed()
                    print("[SUCCESS] Session is valid! Logged in without re-authentication.")
                    return True

                except Exception as e:
                    print(f"[WARNING] Session expired or invalid: {str(e)[:100]}")
                    print("[INFO] Will create new session...")
                    # Delete corrupted session
                    try:
                        os.remove(self.session_file)
                    except:
                        pass

                    # IMPORTANT: Wait before new login attempt after failed session
                    print("[INFO] Waiting 30 seconds before new login attempt...")
                    time.sleep(30)

            # Create new session (only if no valid session found)
            print(f"[INFO] Logging in to Instagram as @{self.username}...")
            print("[INFO] Please wait 15-20 seconds...")

            # Login with proper error handling
            self.client.login(self.username, self.password)

            # Verify login succeeded
            user_id = self.client.user_id
            print(f"[SUCCESS] Login successful! User ID: {user_id}")

            # Save session for future use
            os.makedirs(os.path.dirname(self.session_file), exist_ok=True)
            self.client.dump_settings(self.session_file)
            print(f"[INFO] Session saved to: {self.session_file}")

            return True

        except ChallengeRequired as e:
            print(f"\n[ERROR] Instagram Challenge Required!")
            print(f"Details: {e}")
            print("\n[ACTION REQUIRED]:")
            print("1. Open Instagram app on your phone")
            print("2. Login with your Instagram account")
            print("3. Complete any security challenges (2FA, CAPTCHA, etc.)")
            print("4. Wait 10-15 minutes")
            print("5. Try running the bot again")
            return False

        except PleaseWaitFewMinutes as e:
            print(f"\n[ERROR] Instagram Rate Limit Hit!")
            print(f"Details: {e}")
            print("\n[ACTION REQUIRED]:")
            print("Instagram has temporarily blocked login attempts.")
            print("Wait at least 30-60 minutes before trying again.")
            print("Multiple quick login attempts will extend the block.")
            return False

        except Exception as e:
            error_msg = str(e).lower()

            if "password" in error_msg or "incorrect" in error_msg:
                print(f"\n[ERROR] Authentication Failed!")
                print(f"Details: {e}")
                print("\n[POSSIBLE CAUSES]:")
                print("1. Password might be incorrect")
                print("2. Account has 2FA enabled (disable it for bot)")
                print("3. IP address is temporarily blocked by Instagram")
                print("4. Account requires verification")
                print("\n[SOLUTIONS]:")
                print("1. Verify password by logging in manually at instagram.com")
                print("2. Wait 1-2 hours if multiple login attempts were made")
                print("3. Try from a different network/device")
                print("4. Check if account is locked or suspended")

            elif "ip" in error_msg or "blacklist" in error_msg:
                print(f"\n[ERROR] IP Address Blocked by Instagram!")
                print(f"Details: {e}")
                print("\n[WHY THIS HAPPENS]:")
                print("- Multiple automated login attempts detected")
                print("- Instagram anti-bot protection triggered")
                print("- Suspicious activity from your IP")
                print("\n[SOLUTIONS]:")
                print("1. WAIT: 2-4 hours minimum (MOST IMPORTANT)")
                print("2. CHANGE IP: Restart router or use different network")
                print("3. USE MOBILE: Try with phone's mobile data")
                print("4. VERIFY ACCOUNT: Login manually on phone first")

            else:
                print(f"\n[ERROR] Unexpected login error!")
                print(f"Details: {e}")
                print("\n[TRY]:")
                print("1. Wait 1 hour and try again")
                print("2. Check Instagram app for any notifications")
                print("3. Verify account is not suspended")

            return False

    def upload_reel(
        self,
        video_path: str,
        caption: str,
        hashtags: Optional[list] = None,
        thumbnail_path: Optional[str] = None
    ) -> bool:
        """
        Upload a video as Instagram Reel.

        Args:
            video_path: Path to video file
            caption: Reel caption
            hashtags: List of hashtags (without #)
            thumbnail_path: Optional custom thumbnail

        Returns:
            True if upload successful, False otherwise
        """
        try:
            # Verify video exists
            if not os.path.exists(video_path):
                print(f"[ERROR] Video not found: {video_path}")
                return False

            # Build full caption with hashtags
            full_caption = caption
            if hashtags:
                hashtag_str = " ".join([f"#{tag}" for tag in hashtags])
                full_caption = f"{caption}\n\n{hashtag_str}"

            print("\n" + "=" * 60)
            print("UPLOADING REEL TO INSTAGRAM")
            print("=" * 60)
            print(f"Video: {video_path}")
            print(f"Caption: {caption}")
            if hashtags:
                print(f"Hashtags: {', '.join(hashtags)}")
            print("=" * 60)

            # Upload the reel
            print("[INFO] Uploading reel to Instagram...")
            media = self.client.clip_upload(
                path=video_path,
                caption=full_caption,
                thumbnail=thumbnail_path if thumbnail_path else None
            )

            print("\n" + "=" * 60)
            print("[SUCCESS] REEL UPLOADED SUCCESSFULLY!")
            print(f"Media ID: {media.pk}")
            print(f"Media Code: {media.code}")
            print(f"Instagram URL: https://www.instagram.com/reel/{media.code}/")
            print("=" * 60 + "\n")

            # Log upload to history
            self._log_upload(video_path, caption, media.code)

            return True

        except Exception as e:
            print(f"\n[ERROR] Failed to upload reel: {e}")
            return False

    def _log_upload(self, video_path: str, caption: str, media_code: str):
        """
        Log upload to history file.

        Args:
            video_path: Path to uploaded video
            caption: Video caption
            media_code: Instagram media code
        """
        try:
            history_file = "data/upload_history.json"

            # Load existing history
            if os.path.exists(history_file):
                with open(history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            else:
                history = []

            # Add new entry
            entry = {
                "timestamp": datetime.now().isoformat(),
                "video_path": video_path,
                "caption": caption,
                "media_code": media_code,
                "instagram_url": f"https://www.instagram.com/reel/{media_code}/",
                "username": self.username
            }
            history.append(entry)

            # Save history
            os.makedirs(os.path.dirname(history_file), exist_ok=True)
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)

            print(f"[INFO] Upload logged to: {history_file}")

        except Exception as e:
            print(f"[WARNING] Failed to log upload: {e}")

    def logout(self):
        """Logout from Instagram."""
        try:
            self.client.logout()
            print("[INFO] Logged out from Instagram")
        except Exception as e:
            print(f"[WARNING] Logout failed: {e}")


def upload_to_instagram(
    video_path: str,
    caption: str,
    username: str = None,
    password: str = None,
    hashtags: list = None
) -> bool:
    """
    Convenience function to upload a reel to Instagram.

    Args:
        video_path: Path to video file
        caption: Reel caption
        username: Instagram username (from env if not provided)
        password: Instagram password (from env if not provided)
        hashtags: List of hashtags

    Returns:
        True if upload successful, False otherwise
    """
    # Get credentials from environment if not provided
    if not username:
        username = os.getenv("INSTAGRAM_USERNAME")
    if not password:
        password = os.getenv("INSTAGRAM_PASSWORD")

    if not username or not password:
        print("[ERROR] Instagram credentials not provided!")
        print("[INFO] Set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD in .env file")
        return False

    # Default hashtags if not provided
    if not hashtags:
        hashtags = [
            "technews",
            "tech",
            "technology",
            "ai",
            "innovation",
            "trending",
            "reels",
            "viral"
        ]

    try:
        # Create uploader instance
        uploader = InstagramUploader(username, password)

        # Login
        if not uploader.login():
            return False

        # Upload reel
        success = uploader.upload_reel(
            video_path=video_path,
            caption=caption,
            hashtags=hashtags
        )

        return success

    except Exception as e:
        print(f"[ERROR] Upload process failed: {e}")
        return False


# Example usage
if __name__ == "__main__":
    # Test upload
    test_video = "data/output/news_reel_20251220_024036.mp4"
    test_caption = "🚀 Google Pixel just got an emoji upgrade! Now matching iPhone's sleek emoji designs. Tech news getting more exciting! 📱✨"

    success = upload_to_instagram(
        video_path=test_video,
        caption=test_caption
    )

    if success:
        print("\n✅ Test upload completed successfully!")
    else:
        print("\n❌ Test upload failed!")
