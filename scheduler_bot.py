"""
Automated Instagram News Reel Bot Scheduler

This script runs the news reel bot on a schedule and automatically
uploads to Instagram at specified times.

Features:
- Daily scheduled posts at specific times
- Automatic video generation and upload
- Timezone support
- Error handling and logging
- Can run 24/7 in the background

Usage:
    python scheduler_bot.py

Environment Variables Required:
    - ENABLE_SCHEDULER=true
    - DAILY_POST_TIME=10:00 (HH:MM format)
    - TIMEZONE=UTC (or your timezone)
    - INSTAGRAM_USERNAME=your_username
    - INSTAGRAM_PASSWORD=your_password

Author: AI News Reel Bot
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import main  # Import the main module
from src.scheduler_manager import SchedulerManager
from src.uploader import upload_to_instagram


def scheduled_post_job():
    """
    Main job function that runs on schedule.
    Generates a news reel and uploads it to Instagram.
    """
    print("\n" + "=" * 70)
    print("SCHEDULED JOB STARTED")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70 + "\n")

    try:
        # Generate news reel
        print("[STEP 1/2] Generating news reel...")
        success = main.main()  # Call the correct function

        if not success:
            print("[ERROR] Failed to generate news reel")
            return

        # Get the latest video file
        output_dir = "data/output"
        video_files = [f for f in os.listdir(output_dir) if f.endswith('.mp4')]

        if not video_files:
            print("[ERROR] No video file found in output directory")
            return

        # Get most recent video
        video_files.sort(reverse=True)
        latest_video = os.path.join(output_dir, video_files[0])

        print(f"[OK] Video generated: {latest_video}")

        # Upload to Instagram
        print("\n[STEP 2/2] Uploading to Instagram...")

        # Read caption from script (simplified version)
        caption = "🚀 Breaking Tech News! Stay updated with the latest in technology. Follow for daily tech updates! 📱✨"

        upload_success = upload_to_instagram(
            video_path=latest_video,
            caption=caption
        )

        if upload_success:
            print("\n" + "=" * 70)
            print("[SUCCESS] SCHEDULED POST COMPLETED!")
            print(f"Video uploaded to Instagram successfully!")
            print("=" * 70 + "\n")
        else:
            print("\n[WARNING] Video generated but upload failed")
            print(f"Manual upload required: {latest_video}\n")

    except Exception as e:
        print(f"\n[ERROR] Scheduled job failed: {e}")
        import traceback
        traceback.print_exc()


def main():
    """
    Main function to start the scheduler.
    """
    print("\n" + "=" * 70)
    print("AUTOMATED INSTAGRAM NEWS REEL BOT - SCHEDULER")
    print("=" * 70 + "\n")

    # Check if scheduler is enabled
    scheduler_enabled = os.getenv("ENABLE_SCHEDULER", "false").lower() == "true"

    if not scheduler_enabled:
        print("[ERROR] Scheduler is disabled!")
        print("[INFO] Set ENABLE_SCHEDULER=true in .env file to enable scheduling")
        print("\nTo run the bot once without scheduling, use: python main.py\n")
        return

    # Get schedule configuration
    daily_time = os.getenv("DAILY_POST_TIME", "10:00")
    timezone = os.getenv("TIMEZONE", "UTC")

    # Validate Instagram credentials
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")

    if not username or not password or username == "your_instagram_username":
        print("[ERROR] Instagram credentials not configured!")
        print("[INFO] Set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD in .env file")
        return

    # Parse daily time
    try:
        hour, minute = map(int, daily_time.split(":"))
    except:
        print(f"[ERROR] Invalid DAILY_POST_TIME format: {daily_time}")
        print("[INFO] Use HH:MM format (e.g., 10:00, 18:30)")
        return

    # Validate timezone
    try:
        import pytz
        pytz.timezone(timezone)
    except:
        print(f"[ERROR] Invalid TIMEZONE: {timezone}")
        print("[INFO] Use valid timezone (e.g., UTC, America/New_York, Asia/Kolkata)")
        return

    print("[INFO] Scheduler Configuration:")
    print(f"  Daily Post Time: {daily_time} ({timezone})")
    print(f"  Instagram Account: @{username}")
    print("\n" + "=" * 70 + "\n")

    # Create scheduler
    scheduler = SchedulerManager(timezone=timezone, background=False)

    # Schedule daily job
    scheduler.add_daily_job(
        job_func=scheduled_post_job,
        hour=hour,
        minute=minute,
        job_id="daily_instagram_post"
    )

    # Optional: Add test job (runs immediately for testing)
    # Uncomment the line below to test the job immediately
    # scheduler.add_interval_job(scheduled_post_job, seconds=10, job_id="test_post")

    print("[INFO] Scheduler is ready!")
    print("[INFO] The bot will automatically generate and post videos daily")
    print("[INFO] Press Ctrl+C to stop the scheduler\n")

    # Start scheduler (blocking)
    scheduler.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] Scheduler stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Scheduler failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
