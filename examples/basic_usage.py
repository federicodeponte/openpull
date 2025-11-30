"""Example usage of the FlexibleScraper."""

import asyncio
import os
from dotenv import load_dotenv
from crawl4ai_scraper import FlexibleScraper

load_dotenv()


async def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment")
        return

    scraper = FlexibleScraper(api_key)

    # Example 1: Simple extraction
    print("=" * 50)
    print("Example 1: Extract company info from a website")
    print("=" * 50)

    result = await scraper.scrape(
        url="https://anthropic.com",
        prompt="Extract the company name, tagline, and main product offerings",
    )
    print(f"Result: {result}")

    # Example 2: Extract with schema
    print("\n" + "=" * 50)
    print("Example 2: Extract with structured schema")
    print("=" * 50)

    schema = {
        "type": "object",
        "properties": {
            "company_name": {"type": "string"},
            "products": {"type": "array", "items": {"type": "string"}},
            "contact_email": {"type": "string"},
        },
    }

    result = await scraper.scrape(
        url="https://openai.com",
        prompt="Extract company information",
        schema=schema,
    )
    print(f"Result: {result}")

    # Example 3: Extract links only
    print("\n" + "=" * 50)
    print("Example 3: Extract links from a page")
    print("=" * 50)

    result = await scraper.scrape(
        url="https://news.ycombinator.com",
        prompt="",  # Not needed for link extraction
        extract_links=True,
    )
    print(f"Total links: {result.get('total_links', 0)}")
    print(f"Internal links: {len(result.get('internal_links', []))}")
    print(f"External links: {len(result.get('external_links', []))}")


if __name__ == "__main__":
    asyncio.run(main())
