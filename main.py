"""
Automated AI News Reel Bot - Main Orchestration Script
Creates 9:16 vertical videos for Instagram from trending tech news
"""

import os
import sys
from datetime import datetime

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Import custom modules
from src.validate_api import validate_api_keys
from src.fetcher import get_reddit_news
from src.scripter import generate_script
from src.generator import generate_audio, generate_images
from src.editor import create_video


def main():
    """
    Main pipeline for automated video generation.

    Pipeline:
    1. Validate API keys
    2. Fetch trending news from NewsAPI
    3. Generate script with Google Gemini
    4. Create audio with EdgeTTS (FREE!)
    5. Generate images with Gradients/Pexels
    6. Assemble video with MoviePy
    """

    # Step 0: Validate API keys before starting
    is_valid, _ = validate_api_keys()

    if not is_valid:
        print("\n" + "=" * 70)
        print("[FAILED] CANNOT START - API Keys Not Configured")
        print("=" * 70)
        print("\nPlease fix the errors above and run again.")
        print("Need help? Check README.md for setup instructions.")
        print("=" * 70)
        return False

    print("\n" + "=" * 70)
    print(" " * 15 + "AUTOMATED AI NEWS REEL BOT")
    print("=" * 70)
    print()

    # Configuration
    SUBREDDIT = os.getenv("SUBREDDIT", "technology")
    POST_LIMIT = int(os.getenv("POST_LIMIT", "1"))

    # File paths
    AUDIO_PATH = "data/temp/audio.mp3"
    IMAGE_FOLDER = "data/temp"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    OUTPUT_PATH = f"data/output/news_reel_{timestamp}.mp4"

    try:
        # ========================================================================
        # STEP 1: Fetch News from Reddit
        # ========================================================================
        print("STEP 1: Fetching trending news from Reddit")
        print("-" * 70)
        print(f"Subreddit: r/{SUBREDDIT}")
        print(f"Fetching top {POST_LIMIT} post(s)...\n")

        news_posts = get_reddit_news(subreddit_name=SUBREDDIT, limit=POST_LIMIT)

        if not news_posts:
            print("[ERROR] Failed to fetch news from NewsAPI")
            print("  Check your NewsAPI credentials in .env file")
            return False

        # Use the first post
        selected_post = news_posts[0]
        print(f"[OK] Selected post: {selected_post['title'][:60]}...")
        print(f"  Post ID: {selected_post['post_id']}")
        print()

        # ========================================================================
        # STEP 2: Generate Script with GPT-4o
        # ========================================================================
        print("STEP 2: Generating viral script with OpenAI GPT-4o")
        print("-" * 70)

        script_data = generate_script(selected_post)

        if not script_data:
            print("[ERROR] Failed to generate script")
            print("  Check your Gemini API key in .env file")
            return False

        print(f"[OK] Script generated successfully!")
        print(f"  Hook: {script_data['hook'][:50]}...")
        print(f"  Body length: {len(script_data['body'])} characters")
        print(f"  Image prompts: {len(script_data['image_prompts'])} prompts")
        print()

        # Combine hook and body for full narration
        full_script = f"{script_data['hook']} {script_data['body']}"

        # ========================================================================
        # STEP 3: Generate Audio with EdgeTTS (FREE!)
        # ========================================================================
        print("STEP 3: Generating audio with EdgeTTS (Microsoft Text-to-Speech)")
        print("-" * 70)

        audio_success = generate_audio(full_script, AUDIO_PATH)

        if not audio_success:
            print("[ERROR] Failed to generate audio")
            print("  Make sure edge-tts is installed: pip install edge-tts")
            return False

        print(f"[OK] Audio generated: {AUDIO_PATH}")
        print()

        # ========================================================================
        # STEP 4: Generate Images (Gradients or Pexels)
        # ========================================================================
        print("STEP 4: Generating images (Gradients/Pexels)")
        print("-" * 70)

        image_paths = generate_images(script_data['image_prompts'], IMAGE_FOLDER)

        if not image_paths or len(image_paths) != len(script_data['image_prompts']):
            print(f"[ERROR] Failed to generate all images")
            print(f"  Expected: {len(script_data['image_prompts'])}, Got: {len(image_paths)}")
            print("  Check image generation settings")
            return False

        print(f"[OK] Generated {len(image_paths)} images successfully")
        print()

        # ========================================================================
        # STEP 5: Assemble Video with MoviePy
        # ========================================================================
        print("STEP 5: Assembling video with MoviePy")
        print("-" * 70)

        video_success = create_video(
            audio_path=AUDIO_PATH,
            image_folder_path=IMAGE_FOLDER,
            output_path=OUTPUT_PATH,
            captions=script_data['image_prompts']
        )

        if not video_success:
            print("[ERROR] Failed to create video")
            print("  Check MoviePy installation and file permissions")
            return False

        # ========================================================================
        # SUCCESS
        # ========================================================================
        print("\n" + "=" * 70)
        print(" " * 20 + "[SUCCESS]!")
        print("=" * 70)
        print(f"\nVideo generated successfully at: {OUTPUT_PATH}")
        print(f"\nPost details:")
        print(f"  Title: {selected_post['title']}")
        print(f"  Source: {selected_post['post_id']}")
        print(f"\nVideo specifications:")
        print(f"  Resolution: 1080x1920 (9:16 vertical)")
        print(f"  Format: MP4")
        print(f"  Ready for Instagram Reels!")
        print("\n" + "=" * 70 + "\n")

        return True

    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] Process interrupted by user")
        return False

    except Exception as e:
        print(f"\n[ERROR] UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def cleanup_temp_files():
    """
    Optional: Clean up temporary files after video generation
    """
    import glob

    temp_files = [
        "data/temp/audio.mp3",
        *glob.glob("data/temp/image_*.png")
    ]

    for file_path in temp_files:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Cleaned up: {file_path}")
        except Exception as e:
            print(f"Could not remove {file_path}: {e}")


if __name__ == "__main__":
    """
    Entry point for the bot
    """

    # Run the main pipeline
    success = main()

    # Optional: Uncomment to clean up temp files after generation
    # if success:
    #     print("\nCleaning up temporary files...")
    #     cleanup_temp_files()

    # Exit with appropriate status code
    sys.exit(0 if success else 1)
