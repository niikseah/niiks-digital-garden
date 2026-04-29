"""Core workflow helpers for the HeyMax data extraction pipeline."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Callable, Dict, Iterable, List, Optional, Union

from scraper.instagram_reel_extractor import extract_instagram_content
from scraper.instagram_post_extractor import extract_instagram_post_content
from scraper.tiktok_extractor import extract_tiktok_content
from scraper.youtube_extracter import extract_youtube_content

Extractor = Callable[[str], Dict[str, Any]]

# Maps platform names to respective extractor function.
PLATFORM_EXTRACTORS: Dict[str, Extractor] = {
    "youtube": extract_youtube_content,
    "instagram": extract_instagram_content,
    "instagram_reel": extract_instagram_content,
    "instagram_post": extract_instagram_post_content,
    "tiktok": extract_tiktok_content,
}


def run_extractor(platform: str, url: str, extractor: Optional[Extractor]) -> Dict[str, Any]:
    """Run given extractor on the URL to return extraction result."""
    print(f"Running extractor for {platform}: {url[:50]}...")
    
    if extractor is None:
        # Treat unsupported platforms (e.g., Airbnb) as intentionally skipped, not errors.
        print(f"  No extractor available for {platform}, skipping")
        return {
            "platform": platform,
            "url": url,
            "status": "skipped",
            "text": "",
        }
    try:
        print(f"  Calling extractor function...")
        result = extractor(url)
        print(f"  Extractor returned: status={result.get('status', 'unknown')}, text_length={len(result.get('text', ''))}")
        
        # Check for errors in result
        if result.get("status") == "error":
            error_msg = result.get("error", "Unknown error")
            print(f"  ⚠️ Extraction error: {error_msg}")
        elif not result.get("text"):
            print(f"  ⚠️ No transcript extracted (empty text)")
        else:
            print(f"  ✅ Successfully extracted transcript")
            
    except Exception as exc:  # pragma: no cover - network failure path
        print(f"  ❌ Exception during extraction: {exc}")
        import traceback
        traceback.print_exc()
        return {
            "platform": platform,
            "url": url,
            "status": "error",
            "text": "",
            "error": f"Extractor error: {exc}",
        }

    if "platform" not in result:
        result["platform"] = platform
    if "url" not in result:
        result["url"] = url
    return result


def _normalise_created_time(value: Union[str, int, float, None]) -> Optional[str]:
    """Normalize common time representations to ISO8601 'YYYY-MM-DDTHH:MM:SS.000Z'."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        try:
            dt = datetime.utcfromtimestamp(value)
            return dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        except Exception:  # pragma: no cover
            return None
    if isinstance(value, str):
        raw = value.strip()
        if not raw:
            return None
        # Quick path: already ISO with Z
        if "T" in raw and raw.endswith("Z"):
            try:
                # Trim fractional part if present and reformat with .000Z
                base = raw.split(".")[0].rstrip("Z")
                dt = datetime.strptime(base, "%Y-%m-%dT%H:%M:%S")
                return dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")
            except Exception:
                pass
        # Try a few common formats
        for fmt in (
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
        ):
            try:
                dt = datetime.strptime(raw, fmt)
                return dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")
            except Exception:
                continue
        return None
    return None


def extract_metadata_from_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """Return only canonical metadata keys: 'author' and 'createdTime'."""
    author: Optional[str] = None
    created_raw: Optional[Union[str, int, float]] = None

    sources: List[Dict[str, Any]] = []
    if isinstance(result.get("metadata"), dict):
        sources.append(result["metadata"])
    if isinstance(result.get("data"), dict):
        sources.append(result["data"])
    sources.append(result)

    author_keys = (
        "author",
        "authorName",
        "author_name",
        "username",
        "ownerUsername",
        "owner",
        "user",
        "channel",
        "channel_name",
    )
    time_keys = (
        "createdTime",
        "createTime",
        "create_time",
        "createTimeISO",
        "published_at",
        "publishedAt",
        "timestamp",
        "taken_at",
        "takenAt",
        "time",
    )

    for src in sources:
        if author is None:
            for k in author_keys:
                v = src.get(k)
                if isinstance(v, str) and v.strip():
                    author = v.strip()
                    break
        if created_raw is None:
            for k in time_keys:
                if k in src:
                    created_raw = src.get(k)
                    break

    created = _normalise_created_time(created_raw)
    return {"author": author or None, "createdTime": created or None}


def build_link_payload(result: Dict[str, Any]) -> Dict[str, Any]:
    """Builds output in canonical schema with strict key casing and selection."""
    metadata = extract_metadata_from_result(result)

    transcript_value = result.get("text")
    if not isinstance(transcript_value, str):
        transcript_value = ""

    # Drop None values from metadata; if nothing remains, use empty object.
    clean_meta = {k: v for k, v in metadata.items() if v is not None}
    
    # Include status and error if present
    payload = {
        "link": {
            "platform": result.get("platform"),
            "url": result.get("url"),
            "transcript": transcript_value,
            "metadata": clean_meta if clean_meta else {},
        }
    }
    
    # Add status and error information if available
    if "status" in result:
        payload["link"]["status"] = result["status"]
    if "error" in result:
        payload["link"]["error"] = result["error"]

    return payload


def process_links_batch(links_map: Dict[str, List[str]]) -> List[Dict[str, Any]]:
    """Extract transcripts from a dict of links. Returns list of link payloads."""
    outputs: List[Dict[str, Any]] = []
    for platform_label, urls in links_map.items():
        normalized_platform = platform_label.strip().lower()  # Normalize platform name to lower case
        extractor = PLATFORM_EXTRACTORS.get(normalized_platform)  # Get extractor function for respective platform

        for url in urls:
            result = run_extractor(normalized_platform, url, extractor)
            outputs.append(build_link_payload(result))

    return outputs


if __name__ == "__main__":
    import sys
    import os
    import json
    
    # Add project root to path to allow imports
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from utils.link_classifier import classify_link

    print("🔗 HeyMax Extraction Workflow CLI")
    print("-" * 50)
    
    url = input("Enter URL to process: ").strip()
    
    if not url:
        print("❌ No URL provided.")
        exit(1)

    print(f"\n🔍 Classifying URL...")
    platform = classify_link(url)
    print(f"   Platform: {platform}")
    
    if platform == "unknown":
        print("❌ Unknown platform. Supported: youtube, instagram (post/reel), tiktok")
        exit(1)

    print(f"\n🚀 Starting extraction for {platform}...")
    
    # Prepare input for process_links_batch
    links_map = {platform: [url]}
    
    try:
        results = process_links_batch(links_map)
        
        print("\n📊 Extraction Results:")
        print("-" * 50)
        print(json.dumps(results, indent=2, ensure_ascii=False))
        print("-" * 50)
        
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        import traceback
        traceback.print_exc()

