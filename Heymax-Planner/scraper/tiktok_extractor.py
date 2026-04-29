import requests

from utils.apify_client_config import client as default_client

# As extracter returns vtt subtitle file
def _parse_vtt(vtt_text: str) -> str:
    """Convert VTT subtitle content into a plain text transcript."""
    lines = []
    for raw_line in vtt_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("WEBVTT") or "-->" in line:
            continue
        lines.append(line)
    return " ".join(lines)


def _pick_best_subtitle_link(subtitle_links):
    """Return the subtitle entry matching English if available."""

    if not subtitle_links:
        return None

    # Prefer ISO 639 language codes that indicate English.
    preferred_prefixes = ("eng", "en")
    for prefix in preferred_prefixes:
        for entry in subtitle_links:
            lang = (entry.get("language") or "").lower()
            if lang.startswith(prefix):
                return entry

    return subtitle_links[0]


def extract_tiktok_content(url: str, api_client=default_client):
    """Fetch TikTok subtitles via the Apify TikTok Scraper actor."""
    
    if api_client is None:
        return {
            "platform": "tiktok",
            "url": url,
            "status": "error",
            "error": "Apify client not initialized. APIFY_TOKEN is missing.",
            "text": "",
        }
    
    # Only extract transcripts, do not download videos
    run_input = {
        "postURLs": [url],
        "resultsPerPage": 1,
        "shouldDownloadSubtitles": True,
        "shouldDownloadVideos": False,  # Explicitly disable video downloads - only transcripts needed
        "proxyCountryCode": "None",
    }

    try:
        print(f"  Starting TikTok Apify actor: clockworks/tiktok-scraper")
        run = api_client.actor("clockworks/tiktok-scraper").call(run_input=run_input)
        print(f"  Run started: {run.get('id', 'unknown')}")
        dataset = api_client.dataset(run["defaultDatasetId"])
        print(f"  Dataset ID: {run['defaultDatasetId']}")
    except Exception as exc:
        print(f"  ❌ TikTok extraction failed: {exc}")
        import traceback
        traceback.print_exc()
        return {
            "platform": "tiktok",
            "url": url,
            "status": "error",
            "error": f"Failed to start TikTok scraper actor: {exc}",
            "text": "",
        }

    for item in dataset.iterate_items():
        subtitles = item.get("subtitles") or []
        transcript_language = None
        transcript = " ".join(
            snippet.get("text", "").strip() for snippet in subtitles if snippet.get("text")
        )
        if subtitles:
            transcript_language = next(
                (
                    snippet.get("languageCode")
                    or snippet.get("language")
                    for snippet in subtitles
                    if snippet.get("text")
                ),
                None,
            )
        transcript_source = "inline"

        if not transcript:
            subtitle_links = item.get("videoMeta", {}).get("subtitleLinks") or []
            chosen_link = _pick_best_subtitle_link(subtitle_links)
            download_link = chosen_link.get("downloadLink") if chosen_link else None
            if download_link:
                response = requests.get(download_link, timeout=15)
                response.raise_for_status()

                # Requests may default to ISO-8859-1 which garbles non-ASCII VTT captions.
                try:
                    vtt_text = response.content.decode("utf-8")
                except UnicodeDecodeError:
                    fallback_encoding = response.encoding or response.apparent_encoding or "utf-8"
                    vtt_text = response.content.decode(fallback_encoding, errors="ignore")

                transcript = _parse_vtt(vtt_text)
                transcript_source = "vtt"
                if chosen_link:
                    transcript_language = chosen_link.get("language")

        payload = {
            "platform": "tiktok",
            "url": url,
            "text": transcript,
            "transcript_source": transcript_source,
            "transcript_language": transcript_language,
            "metadata": {
                "id": item.get("id"),
                "author": item.get("authorMeta", {}).get("name"),
                "createTime": item.get("createTimeISO"),
                "music": item.get("musicMeta", {}).get("musicName"),
            },
            "status": "success",
        }
        return payload
    return {
        "platform": "tiktok",
        "url": url,
        "text": "",
        "transcript_source": "none",
        "status": "no_transcript",
    }

