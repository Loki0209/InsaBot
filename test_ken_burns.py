"""
Test script for Ken Burns Effect
Demonstrates the 8 different animation patterns
"""

from src.editor import create_video
import os

print("=" * 70)
print(" " * 15 + "KEN BURNS EFFECT TEST")
print("=" * 70)
print()
print("This script will create a test video showcasing all 8 Ken Burns")
print("animation patterns if you have test audio and images available.")
print()

# Check for test files
audio_path = "data/temp/audio.mp3"
image_folder = "data/temp"
output_path = "data/output/ken_burns_test.mp4"

if not os.path.exists(audio_path):
    print("[ERROR] Test audio not found!")
    print("Please run: python src/generator.py")
    exit(1)

# Check for images
image_files = [f for f in os.listdir(image_folder)
               if f.startswith("image_") and f.endswith(".png")]

if len(image_files) == 0:
    print("[ERROR] No test images found!")
    print("Please run: python src/generator.py")
    exit(1)

print(f"[OK] Found {len(image_files)} test images")
print(f"[OK] Found test audio ({audio_path})")
print()

# Create captions explaining each effect
captions = [
    "ZOOM IN",
    "ZOOM OUT",
    "PAN RIGHT + ZOOM",
    "PAN LEFT + ZOOM",
    "PAN UP + ZOOM",
    "PAN DOWN + ZOOM",
    "DIAGONAL TL + ZOOM",
    "DIAGONAL BR + ZOOM"
]

print("Creating test video with Ken Burns Effect...")
print("Each scene will demonstrate a different animation pattern")
print()

success = create_video(
    audio_path=audio_path,
    image_folder_path=image_folder,
    output_path=output_path,
    captions=captions[:len(image_files)]
)

if success:
    print()
    print("=" * 70)
    print("[SUCCESS] Ken Burns Effect test video created!")
    print(f"Location: {output_path}")
    print()
    print("Watch the video to see all 8 animation patterns in action!")
    print("=" * 70)
else:
    print()
    print("[FAILED] Could not create test video")
    print("Check the error messages above")
