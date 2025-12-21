"""
NewsAPI Data Fetcher Module
Fetches trending tech news from NewsAPI.org
"""

import os
import requests
from dotenv import load_dotenv
from typing import List, Dict, Optional

# Load environment variables from .env file
load_dotenv()


def get_tech_news(category: str = "technology", limit: int = 5) -> List[Dict[str, str]]:
    """
    Fetch top trending tech news from NewsAPI.

    Args:
        category: News category to fetch (default: "technology")
        limit: Number of articles to fetch (default: 5)

    Returns:
        List of dictionaries containing article information:
        - title: Article title
        - description: Article description/summary
        - url: Article URL
        - source: News source name
        - published_at: Publication date
    """

    api_key = os.getenv("NEWSAPI_KEY")

    if not api_key:
        print("[ERROR] NEWSAPI_KEY not found in environment variables")
        return []

    # NewsAPI endpoint for top headlines
    base_url = "https://newsapi.org/v2/top-headlines"

    # Parameters for the request
    params = {
        "apiKey": api_key,
        "category": category,
        "language": "en",
        "pageSize": limit,
        "country": "us"  # You can change to: gb, in, ca, au, etc.
    }

    try:
        print(f"Fetching tech news from NewsAPI...")

        # Make API request
        response = requests.get(base_url, params=params, timeout=10)

        # Check for errors
        if response.status_code != 200:
            print(f"[ERROR] NewsAPI error: {response.status_code}")
            print(f"Response: {response.text}")
            return []

        # Parse JSON response
        data = response.json()

        if data.get("status") != "ok":
            print(f"[ERROR] API returned error: {data.get('message', 'Unknown error')}")
            return []

        articles = data.get("articles", [])

        if not articles:
            print("[ERROR] No articles found")
            return []

        # Format articles data
        news_data = []
        for article in articles:
            # Skip articles without title or description
            if not article.get("title") or article.get("title") == "[Removed]":
                continue

            article_info = {
                "title": article.get("title", "No title"),
                "description": article.get("description", "No description available"),
                "url": article.get("url", ""),
                "source": article.get("source", {}).get("name", "Unknown"),
                "published_at": article.get("publishedAt", ""),
                "content": article.get("content", article.get("description", "No content available"))
            }

            news_data.append(article_info)

        print(f"[OK] Successfully fetched {len(news_data)} articles")
        return news_data

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request error: {e}")
        return []

    except Exception as e:
        print(f"[ERROR] Error fetching news: {e}")
        return []


# Backward compatibility - keep the same function name for main.py
def get_reddit_news(subreddit_name: str = "technology", limit: int = 5) -> List[Dict[str, str]]:
    """
    Wrapper function for backward compatibility with main.py.
    Now fetches from NewsAPI instead of Reddit.
    """
    news_articles = get_tech_news(category="technology", limit=limit)

    # Convert NewsAPI format to match the expected format
    formatted_news = []
    for article in news_articles:
        formatted_news.append({
            "title": article["title"],
            "top_comment": article["description"],  # Use description as context
            "url": article["url"],
            "post_id": article["source"]  # Use source as identifier
        })

    return formatted_news


if __name__ == "__main__":
    """
    Test the fetcher by retrieving tech news from NewsAPI
    """
    print("=" * 60)
    print("Testing NewsAPI Tech News Fetcher")
    print("=" * 60)

    try:
        # Fetch tech news
        print("\nFetching trending tech news...")
        tech_articles = get_tech_news(category="technology", limit=5)

        if tech_articles:
            print(f"\nSuccessfully fetched {len(tech_articles)} articles:\n")

            for idx, article in enumerate(tech_articles, 1):
                print(f"{idx}. Title: {article['title']}")
                print(f"   Source: {article['source']}")
                print(f"   Published: {article['published_at']}")
                print(f"   Description: {article['description'][:100]}..." if len(article['description']) > 100 else f"   Description: {article['description']}")
                print(f"   URL: {article['url']}")
                print("-" * 60)
        else:
            print("\n[FAILED] Failed to fetch news")

        # Test backward compatibility function
        print("\n" + "=" * 60)
        print("Testing backward compatibility wrapper")
        print("=" * 60)

        compat_news = get_reddit_news(limit=3)
        print(f"\n[OK] Fetched {len(compat_news)} articles in compatible format")

        if compat_news:
            print(f"\nFirst article:")
            print(f"  Title: {compat_news[0]['title']}")
            print(f"  Context: {compat_news[0]['top_comment'][:80]}...")

    except Exception as e:
        print(f"\n[ERROR] Error occurred: {e}")
        print("\nMake sure you have:")
        print("1. Created a .env file with NEWSAPI_KEY")
        print("2. Set NEWSAPI_KEY=your_api_key_here")
        print("3. Installed all required packages: pip install -r requirements.txt")
        print("\nGet your free API key at: https://newsapi.org/register")
