"""
Script Generator Module
Uses Google Gemini API to generate viral Instagram scripts from news
"""

import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from typing import Dict, Optional

# Load environment variables from .env file
load_dotenv()


def generate_script(news_data: Dict[str, str]) -> Optional[Dict]:
    """
    Generate a viral Instagram script from news data using Google Gemini API.

    Args:
        news_data: Dictionary containing:
            - title: Post title
            - top_comment: Description/comment for context

    Returns:
        Dictionary with:
            - hook: First 3 seconds of engaging text
            - body: Main explanation (approx 4 sentences)
            - image_prompts: List of 3 image descriptions

        Returns None if generation or parsing fails.
    """

    # Initialize Gemini API
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("[ERROR] GEMINI_API_KEY not found in environment variables")
        return None

    genai.configure(api_key=api_key)

    # Create the model (using gemini-2.5-flash - latest free tier model)
    model = genai.GenerativeModel('gemini-2.5-flash')

    # Combined prompt for Gemini
    prompt = f"""
You are a viral Instagram Tech Influencer. Create a 30-second exciting script based on this tech news:

Title: {news_data.get('title', 'No title')}
Context: {news_data.get('top_comment', 'No context')}

Your response MUST be valid JSON with this exact structure:
{{
  "hook": "The first 3 seconds of text that grabs attention",
  "body": "The main explanation in approximately 4 sentences that educates and entertains",
  "image_prompts": [
    "description for futuristic tech image 1",
    "description for futuristic tech image 2",
    "description for futuristic tech image 3"
  ]
}}

Requirements:
- Hook must be attention-grabbing and under 10 words
- Body should explain the tech news in an exciting, easy-to-understand way
- Each image prompt should describe a visually striking, futuristic scene related to the topic
- Keep it energetic and engaging for a young tech-savvy audience
- Response must be ONLY valid JSON, no additional text before or after
"""

    try:
        # Call Gemini API
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.8,  # Higher creativity for viral content
                max_output_tokens=2048,  # Increased for complete JSON response
            )
        )

        # Extract response content
        response_text = response.text.strip()

        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "").replace("```", "").strip()
        elif response_text.startswith("```"):
            response_text = response_text.replace("```", "").strip()

        # Fix incomplete JSON (sometimes Gemini truncates)
        # If JSON is incomplete, try to close it
        if not response_text.endswith("}"):
            # Find last complete field and close JSON properly
            # Count braces to see if we need to close
            open_braces = response_text.count("{")
            close_braces = response_text.count("}")

            if open_braces > close_braces:
                # JSON is incomplete, try to salvage it
                # Find the last complete array or string
                last_quote = response_text.rfind('"')
                if last_quote > 0:
                    # Truncate to last complete string
                    response_text = response_text[:last_quote + 1]

                    # Close array if needed
                    if response_text.count("[") > response_text.count("]"):
                        response_text += "\n  ]"

                    # Close object
                    response_text += "\n}"

        # Parse JSON response
        try:
            script_data = json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"[WARNING] JSON parsing failed: {e}")
            print(f"[INFO] Response preview: {response_text[:500]}...")
            # Retry with simpler prompt or raise error
            raise ValueError(f"Invalid JSON response from Gemini: {e}")

        # Validate required fields
        required_fields = ["hook", "body", "image_prompts"]
        for field in required_fields:
            if field not in script_data:
                raise ValueError(f"Missing required field: {field}")

        # Validate image_prompts is a list with 3 items
        if not isinstance(script_data["image_prompts"], list):
            raise ValueError("image_prompts must be a list")

        if len(script_data["image_prompts"]) < 3:
            # Pad with generic prompts if less than 3
            while len(script_data["image_prompts"]) < 3:
                script_data["image_prompts"].append("Futuristic technology background with digital elements")
        elif len(script_data["image_prompts"]) > 3:
            # Trim to exactly 3
            script_data["image_prompts"] = script_data["image_prompts"][:3]

        print(f"[OK] Script generated successfully!")
        return script_data

    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON parsing error: {e}")
        print(f"Response was: {response_text if 'response_text' in locals() else 'No response'}")
        return None

    except ValueError as e:
        print(f"[ERROR] Validation error: {e}")
        return None

    except Exception as e:
        print(f"[ERROR] Error generating script: {e}")
        return None


if __name__ == "__main__":
    """
    Test the script generator with sample news data
    """
    print("=" * 60)
    print("Testing Script Generator (Gemini API)")
    print("=" * 60)

    # Sample news data for testing
    sample_news = {
        "title": "Google Announces Gemini 2.0 with Revolutionary AI Capabilities",
        "top_comment": "This is a game changer for AI development. The ability to understand context across text, images, and video simultaneously will revolutionize how we interact with AI systems."
    }

    print("\nInput News Data:")
    print(f"Title: {sample_news['title']}")
    print(f"Comment: {sample_news['top_comment'][:100]}...")
    print("\n" + "-" * 60)

    try:
        # Generate script
        print("\nGenerating script with Google Gemini API...")
        script = generate_script(sample_news)

        if script:
            print("\n[OK] Script Generated Successfully!\n")
            print("=" * 60)
            print("HOOK:")
            print(f"  {script['hook']}")
            print("\nBODY:")
            print(f"  {script['body']}")
            print("\nIMAGE PROMPTS:")
            for idx, prompt in enumerate(script['image_prompts'], 1):
                print(f"  {idx}. {prompt}")
            print("=" * 60)
        else:
            print("\n[FAILED] Failed to generate script")

    except Exception as e:
        print(f"\n[ERROR] Error occurred: {e}")
        print("\nMake sure you have:")
        print("1. Created a .env file with GEMINI_API_KEY")
        print("2. Valid Google Gemini API key")
        print("3. Installed all required packages: pip install -r requirements.txt")
        print("\nGet your free API key at: https://aistudio.google.com/app/apikey")
