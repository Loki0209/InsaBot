"""
List all available EdgeTTS voices.
Run this script to see all voice options for your news reels.
"""

import asyncio
import edge_tts


async def list_voices():
    """List all available voices from EdgeTTS."""
    print("=" * 80)
    print("Available EdgeTTS Voices")
    print("=" * 80)
    print()

    voices = await edge_tts.list_voices()

    # Filter and display English voices
    english_voices = [v for v in voices if v['Locale'].startswith('en-')]

    print(f"Total English voices available: {len(english_voices)}")
    print()

    # Group by locale
    locales = {}
    for voice in english_voices:
        locale = voice['Locale']
        if locale not in locales:
            locales[locale] = []
        locales[locale].append(voice)

    # Display grouped by locale
    for locale in sorted(locales.keys()):
        print(f"\n{locale} ({len(locales[locale])} voices):")
        print("-" * 80)

        for voice in locales[locale]:
            name = voice['ShortName']
            gender = voice['Gender']
            print(f"  {name:<40} ({gender})")

    print("\n" + "=" * 80)
    print("To use a voice, add to your .env file:")
    print("EDGE_TTS_VOICE=en-US-AriaNeural")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(list_voices())
