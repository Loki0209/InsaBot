"""
Video Editor Module
Creates DYNAMIC 9:16 Instagram Reels with Ken Burns Effect, animations, and text overlays

Ken Burns Effect:
- Slow, smooth zoom and pan movements that bring static images to life
- Creates cinematic, professional-looking videos from still images
- Named after documentary filmmaker Ken Burns who popularized this technique
- 8 different animation patterns to keep videos engaging and varied
"""

import os
import sys
from moviepy import (
    ImageClip,
    AudioFileClip,
    TextClip,
    concatenate_videoclips,
    CompositeVideoClip
)
from moviepy.video.fx.FadeIn import FadeIn
from moviepy.video.fx.FadeOut import FadeOut
from typing import List, Optional, Dict
import numpy as np

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def create_zoom_effect(clip, zoom_ratio=0.2, zoom_in=True):
    """
    Create a smooth zoom effect on a clip (in or out).

    Args:
        clip: MoviePy clip
        zoom_ratio: How much to zoom (0.2 = 20% zoom)
        zoom_in: True for zoom in, False for zoom out

    Returns:
        Clip with zoom animation
    """
    def zoom(t):
        # Progressive zoom with easing
        progress = t / clip.duration
        # Apply ease-in-out for smoother animation
        eased_progress = progress * progress * (3 - 2 * progress)

        if zoom_in:
            # Zoom in: from 1.0 to (1.0 + zoom_ratio)
            current_zoom = 1 + (zoom_ratio * eased_progress)
        else:
            # Zoom out: from (1.0 + zoom_ratio) to 1.0
            current_zoom = (1 + zoom_ratio) - (zoom_ratio * eased_progress)

        return current_zoom

    return clip.resized(lambda t: zoom(t))


def create_pan_effect(clip, direction='right', pan_amount=0.1):
    """
    Create a smooth pan effect on a clip with easing.

    Args:
        clip: MoviePy clip
        direction: 'left', 'right', 'up', 'down', 'diagonal_tl', 'diagonal_tr', 'diagonal_bl', 'diagonal_br'
        pan_amount: How much to pan (0.1 = 10% of dimension)

    Returns:
        Clip with pan animation
    """
    w, h = clip.size

    def pan(t):
        progress = t / clip.duration
        # Apply ease-in-out for smoother animation
        eased_progress = progress * progress * (3 - 2 * progress)

        # Calculate pan positions based on direction
        if direction == 'right':
            x = -int(w * pan_amount * eased_progress)
            y = 0
        elif direction == 'left':
            x = int(w * pan_amount * eased_progress)
            y = 0
        elif direction == 'down':
            x = 0
            y = -int(h * pan_amount * eased_progress)
        elif direction == 'up':
            x = 0
            y = int(h * pan_amount * eased_progress)
        elif direction == 'diagonal_tl':  # Top-left
            x = int(w * pan_amount * eased_progress)
            y = int(h * pan_amount * eased_progress)
        elif direction == 'diagonal_tr':  # Top-right
            x = -int(w * pan_amount * eased_progress)
            y = int(h * pan_amount * eased_progress)
        elif direction == 'diagonal_bl':  # Bottom-left
            x = int(w * pan_amount * eased_progress)
            y = -int(h * pan_amount * eased_progress)
        else:  # diagonal_br - Bottom-right
            x = -int(w * pan_amount * eased_progress)
            y = -int(h * pan_amount * eased_progress)

        return (x, y)

    return clip.with_position(pan)


def create_text_overlay(text: str, duration: float, position: str = 'center',
                        fontsize: int = 70, color: str = 'white',
                        stroke_color: str = 'black', stroke_width: int = 3) -> TextClip:
    """
    Create an animated text overlay with stroke.

    Args:
        text: Text to display
        duration: How long to show the text
        position: 'top', 'center', 'bottom'
        fontsize: Font size
        color: Text color
        stroke_color: Outline color
        stroke_width: Outline width

    Returns:
        TextClip with animation
    """
    # Create text clip with bold font
    # Try bold Arial, fall back to regular Arial, then system default
    try:
        txt_clip = TextClip(
            text=text,
            font='Arial-Bold',
            font_size=fontsize,
            color=color,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            text_align='center',
            duration=duration,
            size=(980, None),  # Max width with padding
            method='caption'
        )
    except:
        try:
            txt_clip = TextClip(
                text=text,
                font='Arial',
                font_size=fontsize,
                color=color,
                stroke_color=stroke_color,
                stroke_width=stroke_width,
                text_align='center',
                duration=duration,
                size=(980, None),
                method='caption'
            )
        except:
            # Last resort: use default font without stroke
            txt_clip = TextClip(
                text=text,
                font_size=fontsize,
                color=color,
                text_align='center',
                duration=duration,
                size=(980, None),
                method='caption'
            )

    # Position text
    if position == 'top':
        txt_clip = txt_clip.with_position(('center', 100))
    elif position == 'bottom':
        txt_clip = txt_clip.with_position(('center', 1700))
    else:  # center
        txt_clip = txt_clip.with_position('center')

    # Add fade in/out animations (removed to save memory)
    # txt_clip = txt_clip.with_effects([
    #     FadeIn(0.3),
    #     FadeOut(0.3)
    # ])

    return txt_clip


def create_dynamic_clip(image_path: str, duration: float, index: int,
                       caption: str = None):
    """
    Create a dynamic video clip with animations and text overlay.

    Args:
        image_path: Path to image
        duration: Clip duration
        index: Clip index (for alternating effects)
        caption: Optional text overlay

    Returns:
        Video clip with all effects
    """
    target_width = 1080
    target_height = 1920

    # Create image clip
    img_clip = ImageClip(image_path)

    # Get original dimensions
    img_width, img_height = img_clip.size
    img_aspect = img_height / img_width
    target_aspect = target_height / target_width

    # Resize to fit with extra room for zoom/pan
    # 15% extra for smooth Ken Burns animations
    scale_factor = 1.15

    if img_aspect < target_aspect:
        new_height = int(target_height * scale_factor)
        new_width = int(img_width * (new_height / img_height))
        resized = img_clip.resized(height=new_height)
        # Center crop
        x1 = int((new_width - target_width) / 2)
        y1 = 0
        cropped = resized.cropped(x1=x1, y1=y1, width=target_width, height=target_height)
    else:
        new_width = int(target_width * scale_factor)
        new_height = int(img_height * (new_width / img_width))
        resized = img_clip.resized(width=new_width)
        # Center crop
        x1 = 0
        y1 = int((new_height - target_height) / 2)
        cropped = resized.cropped(x1=x1, y1=y1, width=target_width, height=target_height)

    # Set duration
    cropped = cropped.with_duration(duration)

    # Apply Ken Burns effect with varied animations
    # More diverse effects for engaging videos
    effects = [
        'zoom_in',           # Classic zoom in
        'zoom_out',          # Zoom out (reveals more)
        'pan_right_zoom',    # Pan right + zoom in
        'pan_left_zoom',     # Pan left + zoom in
        'pan_up_zoom',       # Pan up + zoom in
        'pan_down_zoom',     # Pan down + zoom in
        'diagonal_tl_zoom',  # Diagonal top-left + zoom
        'diagonal_br_zoom',  # Diagonal bottom-right + zoom
    ]
    effect = effects[index % len(effects)]

    # Apply the selected Ken Burns effect (optimized ratios for smooth animations)
    if effect == 'zoom_in':
        cropped = create_zoom_effect(cropped, zoom_ratio=0.08, zoom_in=True)
    elif effect == 'zoom_out':
        cropped = create_zoom_effect(cropped, zoom_ratio=0.08, zoom_in=False)
    elif effect == 'pan_right_zoom':
        cropped = create_zoom_effect(cropped, zoom_ratio=0.06, zoom_in=True)
        cropped = create_pan_effect(cropped, direction='right', pan_amount=0.04)
    elif effect == 'pan_left_zoom':
        cropped = create_zoom_effect(cropped, zoom_ratio=0.06, zoom_in=True)
        cropped = create_pan_effect(cropped, direction='left', pan_amount=0.04)
    elif effect == 'pan_up_zoom':
        cropped = create_zoom_effect(cropped, zoom_ratio=0.06, zoom_in=True)
        cropped = create_pan_effect(cropped, direction='up', pan_amount=0.04)
    elif effect == 'pan_down_zoom':
        cropped = create_zoom_effect(cropped, zoom_ratio=0.06, zoom_in=True)
        cropped = create_pan_effect(cropped, direction='down', pan_amount=0.04)
    elif effect == 'diagonal_tl_zoom':
        cropped = create_zoom_effect(cropped, zoom_ratio=0.06, zoom_in=True)
        cropped = create_pan_effect(cropped, direction='diagonal_tl', pan_amount=0.04)
    else:  # diagonal_br_zoom
        cropped = create_zoom_effect(cropped, zoom_ratio=0.06, zoom_in=True)
        cropped = create_pan_effect(cropped, direction='diagonal_br', pan_amount=0.04)

    # Create composite with text overlay if provided
    # TEMPORARILY DISABLED TO FIX MEMORY ERROR - TEXT OVERLAYS CAUSE MASK ISSUES
    # if caption:
    #     # Split long text into multiple lines
    #     words = caption.split()
    #     if len(words) > 6:
    #         mid = len(words) // 2
    #         line1 = ' '.join(words[:mid])
    #         line2 = ' '.join(words[mid:])
    #         caption = f"{line1}\n{line2}"
    #
    #     # Create text overlay
    #     txt_overlay = create_text_overlay(
    #         text=caption.upper(),
    #         duration=duration,
    #         position='bottom',
    #         fontsize=60,
    #         color='white',
    #         stroke_color='black',
    #         stroke_width=4
    #     )
    #
    #     # Composite image + text with optimized settings
    #     composite = CompositeVideoClip([cropped, txt_overlay], size=(1080, 1920))
    #     return composite
    # else:
    #     return cropped

    # Return cropped video without text overlay (temporary fix for memory issues)
    return cropped


def create_video(
    audio_path: str,
    image_folder_path: str,
    output_path: str = "data/output/video.mp4",
    captions: List[str] = None
) -> bool:
    """
    Create a DYNAMIC 9:16 Instagram Reel with animations and text overlays.

    Args:
        audio_path: Path to the audio file (MP3)
        image_folder_path: Path to folder containing images
        output_path: Path to save the final video
        captions: Optional list of captions for each scene

    Returns:
        True if successful, False otherwise
    """

    try:
        print("=" * 60)
        print("Creating DYNAMIC Instagram Reel")
        print("=" * 60)

        # Step 1: Load audio
        print(f"\n[1/6] Loading audio from: {audio_path}")
        if not os.path.exists(audio_path):
            print(f"✗ Audio file not found: {audio_path}")
            return False

        audio_clip = AudioFileClip(audio_path)
        audio_duration = audio_clip.duration
        print(f"✓ Audio loaded: {audio_duration:.2f} seconds")

        # Step 2: Load images
        print(f"\n[2/6] Loading images from: {image_folder_path}")
        image_files = []
        for filename in sorted(os.listdir(image_folder_path)):
            if filename.startswith("image_") and filename.endswith(".png"):
                image_path = os.path.join(image_folder_path, filename)
                image_files.append(image_path)

        if not image_files:
            print(f"✗ No images found in: {image_folder_path}")
            return False

        print(f"✓ Found {len(image_files)} images")
        for img_file in image_files:
            print(f"  - {os.path.basename(img_file)}")

        # Step 3: Calculate durations
        print(f"\n[3/6] Calculating clip durations")
        duration_per_image = audio_duration / len(image_files)
        print(f"✓ Each scene: {duration_per_image:.2f} seconds")

        # Step 4: Create dynamic clips with effects
        print(f"\n[4/6] Creating dynamic clips with animations")
        video_clips = []

        for idx, image_path in enumerate(image_files):
            print(f"Processing scene {idx + 1}/{len(image_files)}: {os.path.basename(image_path)}")

            # Get caption for this scene if available
            caption = captions[idx] if captions and idx < len(captions) else None

            # Create dynamic clip with effects
            clip = create_dynamic_clip(
                image_path=image_path,
                duration=duration_per_image,
                index=idx,
                caption=caption
            )

            video_clips.append(clip)

            # Display applied effect
            effect_names = [
                'Zoom In',
                'Zoom Out',
                'Pan Right + Zoom',
                'Pan Left + Zoom',
                'Pan Up + Zoom',
                'Pan Down + Zoom',
                'Diagonal TL + Zoom',
                'Diagonal BR + Zoom'
            ]
            effect_name = effect_names[idx % len(effect_names)]
            print(f"  [OK] Applied: {effect_name}")

        # Step 5: Concatenate and add audio
        print(f"\n[5/6] Assembling {len(video_clips)} dynamic scenes")
        final_video = concatenate_videoclips(video_clips, method="chain")
        final_video = final_video.with_audio(audio_clip)
        print(f"✓ Video assembled: {final_video.duration:.2f} seconds")

        # Step 6: Export
        print(f"\n[6/6] Exporting dynamic video with Ken Burns Effect to: {output_path}")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        final_video.write_videofile(
            output_path,
            fps=24,  # Reduced from 30 to 24 FPS (still smooth, but faster rendering)
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='data/temp/temp-audio.m4a',
            remove_temp=True,
            preset='ultrafast',  # Changed from 'medium' to 'ultrafast' for 5-10x faster encoding
            bitrate='5000k',  # Reduced from 8000k to 5000k (still good quality, faster encoding)
            threads=8,  # Increased from 4 to 8 threads for better CPU utilization
            logger=None,  # Reduce memory overhead from logging
            write_logfile=False  # Disable log file writing
        )

        print("\n" + "=" * 60)
        print(f"[SUCCESS] DYNAMIC VIDEO CREATED WITH KEN BURNS EFFECT!")
        print(f"Output: {output_path}")
        print(f"Duration: {final_video.duration:.2f} seconds")
        print(f"Resolution: 1080x1920 (9:16)")
        print(f"FPS: 24 (cinematic, optimized)")
        print(f"Effects: Ken Burns (8 patterns), Smooth Animations")
        print(f"Encoding: ULTRAFAST preset for rapid generation")
        print("=" * 60)

        # Cleanup
        audio_clip.close()
        for clip in video_clips:
            clip.close()
        final_video.close()

        return True

    except Exception as e:
        print(f"\n✗ Error creating video: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    """
    Test the dynamic video editor
    """
    print("=" * 60)
    print("Testing Dynamic Video Editor")
    print("=" * 60)

    audio_path = "data/temp/audio.mp3"
    image_folder = "data/temp"
    output_path = "data/output/test_dynamic_video.mp4"

    # Test captions
    test_captions = [
        "Breaking Tech News",
        "AI Revolution",
        "The Future Is Here"
    ]

    print("\nChecking for test files...")

    if not os.path.exists(audio_path):
        print("\n[ERROR] Test audio file not found!")
        print("Run: python src/generator.py")
    else:
        image_count = len([f for f in os.listdir(image_folder)
                          if f.startswith("image_") and f.endswith(".png")])

        if image_count == 0:
            print("\n[ERROR] No test images found!")
            print("Run: python src/generator.py")
        else:
            print(f"[OK] Found audio and {image_count} images")
            print("\nCreating DYNAMIC test video...")

            success = create_video(
                audio_path=audio_path,
                image_folder_path=image_folder,
                output_path=output_path,
                captions=test_captions[:image_count]
            )

            if success:
                print("\n[OK] Dynamic video test PASSED")
                print(f"Check your video at: {output_path}")
            else:
                print("\n[FAILED] Dynamic video test FAILED")