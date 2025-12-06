"""
OpenPull API Service
FastAPI wrapper for OpenPull scraper
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import os
import asyncio
from typing import Optional

from openpull import FlexibleScraper

app = FastAPI(title="OpenPull API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize scraper with API key from environment
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("⚠️  WARNING: GEMINI_API_KEY not set. Scraper will not work without it.")

scraper = None

async def get_scraper():
    """Lazy initialization of scraper"""
    global scraper
    if scraper is None:
        if not GEMINI_API_KEY:
            raise HTTPException(status_code=500, detail="GEMINI_API_KEY not configured")
        scraper = FlexibleScraper(api_key=GEMINI_API_KEY)
    return scraper


class ScrapeRequest(BaseModel):
    url: str = Field(..., description="URL to scrape")
    prompt: Optional[str] = Field(None, description="Optional prompt for LLM extraction")
    schema: Optional[dict] = Field(None, alias="schema", description="Optional JSON schema for structured output")


class ScrapeResponse(BaseModel):
    success: bool
    content: Optional[str] = None
    data: Optional[dict] = None
    error: Optional[str] = None
    url: str


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "openpull-api",
        "gemini_configured": GEMINI_API_KEY is not None,
    }


@app.post("/v1/scrape", response_model=ScrapeResponse)
async def scrape(request: ScrapeRequest):
    """
    Scrape a webpage using OpenPull
    
    Returns scraped content, optionally structured via LLM extraction
    """
    try:
        scraper_instance = await get_scraper()
        
        # Scrape with optional prompt and schema
        result = await scraper_instance.scrape(
            url=request.url,
            prompt=request.prompt,
            schema=request.schema,
        )
        
        # Extract content from result
        # OpenPull returns different formats, handle both
        if isinstance(result, dict):
            content = result.get("content") or result.get("text") or str(result)
            data = result.get("data") or result
        else:
            content = str(result)
            data = None
        
        return ScrapeResponse(
            success=True,
            content=content,
            data=data,
            url=request.url,
        )
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Scrape error for {request.url}: {error_msg}")
        return ScrapeResponse(
            success=False,
            error=error_msg,
            url=request.url,
        )


@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "service": "OpenPull API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "scrape": "/v1/scrape",
        },
        "docs": "/docs",
    }

