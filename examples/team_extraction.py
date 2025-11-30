"""Example: Extract team members from a company website."""

import asyncio
import os
from dotenv import load_dotenv
from crawl4ai_scraper import FlexibleScraper

load_dotenv()


async def main():
    api_key = os.getenv("GEMINI_API_KEY")
    scraper = FlexibleScraper(api_key)

    print("Scraping team members from scaile.tech...")
    print("=" * 50)

    result = await scraper.scrape(
        url="https://scaile.tech",
        prompt="Find all team members. Extract their names, roles/titles, and any other info like LinkedIn URLs or bios.",
        schema={
            "type": "object",
            "properties": {
                "team_members": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "role": {"type": "string"},
                            "linkedin": {"type": "string"},
                            "bio": {"type": "string"},
                        },
                    },
                },
                "company_name": {"type": "string"},
            },
        },
        auto_discover_pages=True,
        max_pages=5,
    )

    print(f"\nCompany: {result.get('company_name', 'N/A')}")
    print(f"Pages scraped: {result.get('_pages_scraped', 1)}")
    print(f"\nTeam Members Found:")
    print("-" * 50)

    team = result.get("team_members", [])
    if team:
        for member in team:
            print(f"  Name: {member.get('name', 'N/A')}")
            print(f"  Role: {member.get('role', 'N/A')}")
            if member.get("linkedin"):
                print(f"  LinkedIn: {member.get('linkedin')}")
            if member.get("bio"):
                print(f"  Bio: {member.get('bio')[:100]}...")
            print()
    else:
        print("  No team members found on the pages scraped.")
        print(f"\n  Raw result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
