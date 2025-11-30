# Contributing to crawl4ai-scraper

Thanks for your interest in contributing! This document outlines how to get started.

## Development Setup

1. Fork and clone the repo:
   ```bash
   git clone https://github.com/YOUR_USERNAME/crawl4ai-scraper.git
   cd crawl4ai-scraper
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   ```

3. Install dev dependencies:
   ```bash
   pip install -e ".[dev]"
   playwright install chromium
   ```

4. Set up your environment:
   ```bash
   cp .env.example .env
   # Add your GEMINI_API_KEY to .env
   ```

## Running Tests

```bash
pytest
```

## Code Style

- Use type hints for all function parameters and return values
- Follow PEP 8 style guidelines
- Keep functions focused and single-purpose
- Add docstrings for public methods

## Pull Request Process

1. Create a new branch for your feature/fix
2. Make your changes with clear commit messages
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a PR with a clear description of changes

## Reporting Issues

When reporting bugs, please include:
- Python version
- OS and version
- Steps to reproduce
- Expected vs actual behavior
- Any error messages

## Feature Requests

Feature requests are welcome! Please describe:
- The use case
- Expected behavior
- Any alternatives you've considered
