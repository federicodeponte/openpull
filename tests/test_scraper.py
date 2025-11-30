"""Tests for FlexibleScraper."""

import pytest
from crawl4ai_scraper import FlexibleScraper, FlexibleScraperError


def test_init_without_api_key():
    """Test that FlexibleScraper raises error without API key."""
    with pytest.raises(FlexibleScraperError, match="GEMINI_API_KEY is required"):
        FlexibleScraper("")


def test_init_with_api_key():
    """Test that FlexibleScraper initializes with API key."""
    scraper = FlexibleScraper("test-api-key")
    assert scraper.api_key == "test-api-key"
    assert scraper.client is not None


@pytest.mark.asyncio
async def test_scrape_example_com():
    """Test scraping example.com (requires valid API key)."""
    import os

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        pytest.skip("GEMINI_API_KEY not set")

    scraper = FlexibleScraper(api_key)
    result = await scraper.scrape(
        url="https://example.com",
        prompt="Extract the main heading",
    )

    assert "_pages_scraped" in result
    assert result["_pages_scraped"] == 1
