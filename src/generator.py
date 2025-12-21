"""
Media Generator Module
Handles audio generation (EdgeTTS) and image generation (Pexels/Unsplash)
"""

import os
import requests
from dotenv import load_dotenv
from typing import List, Optional
from PIL import Image, ImageDraw, ImageFont
import io
import asyncio
import edge_tts

# Load environment variables from .env file
load_dotenv()


def generate_audio(text: str, output_path: str = "data/temp/audio.mp3") -> bool:
    """
    Generate audio from text using EdgeTTS (Microsoft Edge Text-to-Speech).
    Completely FREE with no API limits and very realistic voices!

    Args:
        text: The script text to convert to speech
        output_path: Path to save the MP3 file (default: data/temp/audio.mp3)

    Returns:
        True if successful, False otherwise
    """

    # Get voice from environment or use default
    voice = os.getenv("EDGE_TTS_VOICE", "en-US-AriaNeural")

    try:
        print(f"Generating audio with EdgeTTS (Voice: {voice})...")

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Run the async TTS function
        asyncio.run(_generate_audio_async(text, output_path, voice))

        print(f"[SUCCESS] Audio saved to: {output_path}")
        return True

    except Exception as e:
        print(f"[ERROR] Error generating audio: {e}")
        return False


async def _generate_audio_async(text: str, output_path: str, voice: str):
    """Async function to generate audio using EdgeTTS."""
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)


def generate_images(prompts: List[str], output_dir: str = "data/temp") -> List[str]:
    """
    Generate images from prompts using Pexels API (free stock photos).
    Falls back to creating gradient placeholder images if API fails.

    Args:
        prompts: List of text prompts for image search
        output_dir: Directory to save images (default: data/temp)

    Returns:
        List of file paths to generated images
    """

    pexels_api_key = os.getenv("PEXELS_API_KEY", "")

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    generated_images = []

    for idx, prompt in enumerate(prompts):
        try:
            print(f"Generating image {idx + 1}/{len(prompts)}...")
            print(f"Prompt: {prompt[:60]}...")

            image_path = os.path.join(output_dir, f"image_{idx}.png")

            # Try Pexels API first
            if pexels_api_key:
                success = _download_pexels_image(prompt, image_path, pexels_api_key)
                if success:
                    generated_images.append(image_path)
                    continue

            # Fallback: Create gradient placeholder image
            print("  Creating placeholder image...")
            _create_gradient_image(prompt, image_path, idx)
            print(f"✓ Image saved to: {image_path}")
            generated_images.append(image_path)

        except Exception as e:
            print(f"✗ Error generating image {idx}: {e}")
            continue

    return generated_images


def _download_pexels_image(query: str, output_path: str, api_key: str) -> bool:
    """Download an image from Pexels API."""
    try:
        # Extract keywords from prompt
        keywords = " ".join(query.split()[:5])  # Use first 5 words

        headers = {"Authorization": api_key}
        params = {"query": keywords, "per_page": 1, "orientation": "portrait"}

        response = requests.get(
            "https://api.pexels.com/v1/search",
            headers=headers,
            params=params,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            if data.get("photos"):
                photo_url = data["photos"][0]["src"]["large2x"]

                # Download image
                img_response = requests.get(photo_url, timeout=10)
                if img_response.status_code == 200:
                    with open(output_path, "wb") as f:
                        f.write(img_response.content)
                    print(f"✓ Downloaded from Pexels: {output_path}")
                    return True

        return False

    except Exception as e:
        print(f"  Pexels API failed: {e}")
        return False


def _create_gradient_image(prompt: str, output_path: str, index: int):
    """Create a gradient placeholder image with text."""

    # Create 1024x1024 image
    width, height = 1024, 1024

    # Color schemes for variety
    colors = [
        [(41, 128, 185), (142, 68, 173)],  # Blue to Purple
        [(26, 188, 156), (46, 204, 113)],  # Teal to Green
        [(231, 76, 60), (192, 57, 43)],    # Red gradient
        [(241, 196, 15), (243, 156, 18)],  # Yellow to Orange
        [(52, 152, 219), (155, 89, 182)],  # Light Blue to Purple
    ]

    color_scheme = colors[index % len(colors)]

    # Create gradient
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)

    # Draw gradient
    for y in range(height):
        r = int(color_scheme[0][0] + (color_scheme[1][0] - color_scheme[0][0]) * y / height)
        g = int(color_scheme[0][1] + (color_scheme[1][1] - color_scheme[0][1]) * y / height)
        b = int(color_scheme[0][2] + (color_scheme[1][2] - color_scheme[0][2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Add text overlay
    try:
        # Try to use a nice font
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()

    # Add prompt text (truncated)
    text = prompt[:50] + "..." if len(prompt) > 50 else prompt
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2

    # Draw text with shadow
    draw.text((text_x + 2, text_y + 2), text, fill=(0, 0, 0, 128), font=font)
    draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)

    # Save image
    image.save(output_path, 'PNG')


if __name__ == "__main__":
    """
    Test the media generator with sample data
    """
    print("=" * 60)
    print("Testing Media Generator")
    print("=" * 60)

    # Test 1: Audio Generation
    print("\n" + "=" * 60)
    print("TEST 1: Audio Generation")
    print("=" * 60)

    sample_script = """
    Breaking news in AI! Google just announced Gemini 2.0 with revolutionary capabilities.
    This new model can understand text, images, and video simultaneously.
    The implications for content creation are massive.
    Get ready for the future of AI!
    """

    print("\nGenerating audio from sample script...")
    audio_success = generate_audio(sample_script.strip())

    if audio_success:
        print("✓ Audio generation test PASSED")
    else:
        print("✗ Audio generation test FAILED")
        print("Check if EdgeTTS is properly installed")

    # Test 2: Image Generation
    print("\n" + "=" * 60)
    print("TEST 2: Image Generation")
    print("=" * 60)

    sample_prompts = [
        "Futuristic AI brain with glowing neural networks, digital art style, vibrant colors",
        "Modern tech lab with holographic displays showing data streams, cyberpunk aesthetic",
        "Abstract representation of artificial intelligence, geometric patterns, neon blue and purple"
    ]

    print(f"\nGenerating {len(sample_prompts)} images...")
    generated_paths = generate_images(sample_prompts)

    if len(generated_paths) == len(sample_prompts):
        print(f"\n✓ Image generation test PASSED ({len(generated_paths)} images created)")
        for path in generated_paths:
            print(f"  - {path}")
    else:
        print(f"\n✗ Image generation test PARTIAL ({len(generated_paths)}/{len(sample_prompts)} images)")

    print("\n" + "=" * 60)
    print("Testing Complete")
    print("=" * 60)
