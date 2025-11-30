# crawl4ai-scraper

A flexible web scraper with LLM-powered data extraction using [crawl4ai](https://github.com/unclecode/crawl4ai) and Google Gemini.

## Features

- **Async web scraping** with Playwright/Chromium
- **LLM-based extraction** using Gemini 2.5 Flash
- **Structured output** with JSON schema validation
- **Multi-page discovery** - automatically finds and scrapes relevant pages
- **Link extraction** - get internal/external links from any page

## Installation

```bash
pip install crawl4ai-scraper
```

Or install from source:

```bash
git clone https://github.com/federicodeponte/crawl4ai-scraper.git
cd crawl4ai-scraper
pip install -e .
```

### Prerequisites

Install Playwright browsers:

```bash
playwright install chromium
```

## Quick Start

```python
import asyncio
from crawl4ai_scraper import FlexibleScraper

async def main():
    scraper = FlexibleScraper(api_key="your-gemini-api-key")

    result = await scraper.scrape(
        url="https://example.com",
        prompt="Extract the main heading and description",
    )
    print(result)

asyncio.run(main())
```

## Usage Examples

### Basic Extraction

```python
result = await scraper.scrape(
    url="https://company.com",
    prompt="Extract company name, tagline, and main products",
)
# {'company_name': 'Acme Inc', 'tagline': '...', 'products': [...]}
```

### Structured Schema

```python
schema = {
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
                },
            },
        },
    },
}

result = await scraper.scrape(
    url="https://company.com/about",
    prompt="Find all team members with their roles and LinkedIn URLs",
    schema=schema,
)
```

### Multi-Page Discovery

Automatically discover and scrape relevant pages:

```python
result = await scraper.scrape(
    url="https://company.com",
    prompt="Find all team members",
    auto_discover_pages=True,
    max_pages=5,
)
# Scrapes homepage, then uses LLM to find relevant pages like /about, /team
```

### Link Extraction Only

```python
result = await scraper.scrape(
    url="https://news.ycombinator.com",
    prompt="",  # Not needed for link extraction
    extract_links=True,
)
# {'links': [...], 'internal_links': [...], 'external_links': [...], 'total_links': 123}
```

## API Reference

### `FlexibleScraper(api_key: str)`

Initialize the scraper with your Gemini API key.

### `scrape(url, prompt, **kwargs) -> dict`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | str | required | URL to scrape |
| `prompt` | str | required | What to extract from the page |
| `schema` | dict | None | JSON schema for structured output |
| `max_pages` | int | 1 | Max pages to scrape (with auto_discover) |
| `timeout` | int | 30 | Request timeout in seconds |
| `extract_links` | bool | False | Only extract links, skip LLM |
| `auto_discover_pages` | bool | False | Auto-discover relevant pages |

## Environment Variables

```bash
GEMINI_API_KEY=your-api-key-here
```

Or pass directly to the constructor.

## Development

```bash
# Clone the repo
git clone https://github.com/federicodeponte/crawl4ai-scraper.git
cd crawl4ai-scraper

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Credits

Built with:
- [crawl4ai](https://github.com/unclecode/crawl4ai) - Async web crawler
- [Google Gemini](https://ai.google.dev/) - LLM for extraction
- [Playwright](https://playwright.dev/) - Browser automation
