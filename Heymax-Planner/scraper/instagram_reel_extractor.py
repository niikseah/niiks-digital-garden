"""Instagram transcription via Apify's universal video transcript actor."""

from typing import Any, Dict, Iterable, List, Optional

from utils.apify_client_config import client as default_client


ACTOR_ID = "agentx/video-transcript"
DEFAULT_TARGET_LANG = "None"

# I actually have no idea about this
_LANGUAGE_CHOICES: List[str] = [
    "None",
    "Afrikaans",
    "Albanian",
    "Amharic",
    "Arabic",
    "Armenian",
    "Assamese",
    "Aymara",
    "Azerbaijani",
    "Bambara",
    "Basque",
    "Belarusian",
    "Bengali",
    "Bhojpuri",
    "Bosnian",
    "Bulgarian",
    "Catalan",
    "Cebuano",
    "Chichewa",
    "Chinese (Simplified)",
    "Chinese (Traditional)",
    "Corsican",
    "Croatian",
    "Czech",
    "Danish",
    "Dhivehi",
    "Dogri",
    "Dutch",
    "English",
    "Esperanto",
    "Estonian",
    "Ewe",
    "Filipino",
    "Finnish",
    "French",
    "Frisian",
    "Galician",
    "Georgian",
    "German",
    "Greek",
    "Guarani",
    "Gujarati",
    "Haitian Creole",
    "Hausa",
    "Hawaiian",
    "Hebrew",
    "Hindi",
    "Hmong",
    "Hungarian",
    "Icelandic",
    "Igbo",
    "Ilocano",
    "Indonesian",
    "Irish",
    "Italian",
    "Japanese",
    "Javanese",
    "Kannada",
    "Kazakh",
    "Khmer",
    "Kinyarwanda",
    "Konkani",
    "Korean",
    "Krio",
    "Kurdish (Kurmanji)",
    "Kurdish (Sorani)",
    "Kyrgyz",
    "Lao",
    "Latin",
    "Latvian",
    "Lingala",
    "Lithuanian",
    "Luganda",
    "Luxembourgish",
    "Macedonian",
    "Maithili",
    "Malagasy",
    "Malay",
    "Malayalam",
    "Maltese",
    "Maori",
    "Marathi",
    "Meiteilon (Manipuri)",
    "Mizo",
    "Mongolian",
    "Myanmar",
    "Nepali",
    "Norwegian",
    "Odia (Oriya)",
    "Oromo",
    "Pashto",
    "Persian",
    "Polish",
    "Portuguese",
    "Punjabi",
    "Quechua",
    "Romanian",
    "Russian",
    "Samoan",
    "Sanskrit",
    "Scots Gaelic",
    "Sepedi",
    "Serbian",
    "Sesotho",
    "Shona",
    "Sindhi",
    "Sinhala",
    "Slovak",
    "Slovenian",
    "Somali",
    "Spanish",
    "Sundanese",
    "Swahili",
    "Swedish",
    "Tajik",
    "Tamil",
    "Tatar",
    "Telugu",
    "Thai",
    "Tigrinya",
    "Tsonga",
    "Turkish",
    "Turkmen",
    "Twi",
    "Ukrainian",
    "Urdu",
    "Uyghur",
    "Uzbek",
    "Vietnamese",
    "Welsh",
    "Xhosa",
    "Yiddish",
    "Yoruba",
    "Zulu",
]

_LANGUAGE_LOOKUP: Dict[str, str] = {choice.lower(): choice for choice in _LANGUAGE_CHOICES}
_LANGUAGE_LOOKUP["eng"] = "English"


def _normalise_target_language(value: Optional[str]) -> Optional[str]:
    if value is None:
        return DEFAULT_TARGET_LANG
    canonical = _LANGUAGE_LOOKUP.get(value.strip().lower()) if isinstance(value, str) else None
    return canonical or value


def _join_segments(segments: Optional[List[Dict[str, Any]]]) -> str:
    if not isinstance(segments, list):
        return ""
    parts: List[str] = []
    for segment in segments:
        if not isinstance(segment, dict):
            continue
        snippet = segment.get("text")
        if isinstance(snippet, str) and snippet.strip():
            parts.append(snippet.strip())
    return " ".join(parts)


def _extract_primary_text(item: Dict[str, Any]) -> str:
    source = item.get("source_transcript")
    if isinstance(source, dict):
        if isinstance(source.get("text"), str) and source["text"].strip():
            return source["text"].strip()
        segment_text = _join_segments(source.get("segments"))
        if segment_text:
            return segment_text

    target = item.get("target_transcript")
    if isinstance(target, dict):
        if isinstance(target.get("text"), str) and target["text"].strip():
            return target["text"].strip()
        segment_text = _join_segments(target.get("segments"))
        if segment_text:
            return segment_text

    text_fields: Iterable[str] = (
        item.get("text"),
        item.get("transcript"),
        item.get("translatedText"),
    )
    for candidate in text_fields:
        if isinstance(candidate, str) and candidate.strip():
            return candidate.strip()

    return ""


def extract_instagram_content(
    url: str,
    api_client=default_client,
    *,
    target_lang: str = DEFAULT_TARGET_LANG,
) -> Dict[str, Any]:
    """Fetch an Instagram transcript using the universal video transcript actor."""
    
    if api_client is None:
        return {
            "platform": "instagram_reel",
            "url": url,
            "status": "error",
            "error": "Apify client not initialized. APIFY_TOKEN is missing.",
            "text": "",
        }

    normalised_target_lang = _normalise_target_language(target_lang)
    if normalised_target_lang not in _LANGUAGE_CHOICES:
        return {
            "platform": "instagram_reel",
            "url": url,
            "status": "error",
            "error": (
                "Invalid target language. Supported values include: "
                + ", ".join(_LANGUAGE_CHOICES)
            ),
            "text": "",
        }

    # Only extract transcripts - the agentx/video-transcript actor is designed for transcript extraction only
    # It does not download videos, only extracts transcripts from the video URL
    run_input: Dict[str, Any] = {
        "video_url": url,
        "target_lang": normalised_target_lang,
    }

    try:
        print(f"  Starting Instagram Apify actor: {ACTOR_ID}")
        run = api_client.actor(ACTOR_ID).call(run_input=run_input)
        print(f"  Run started: {run.get('id', 'unknown')}")
        dataset = api_client.dataset(run["defaultDatasetId"])
        print(f"  Dataset ID: {run['defaultDatasetId']}")
    except Exception as exc:  # pragma: no cover - network failure path
        print(f"  ❌ Instagram extraction failed: {exc}")
        import traceback
        traceback.print_exc()
        return {
            "platform": "instagram_reel",
            "url": url,
            "status": "error",
            "error": f"Failed to start Instagram transcript actor: {exc}",
            "text": "",
        }

    for item in dataset.iterate_items():
        if isinstance(item, dict) and item.get("error"):
            return {
                "platform": "instagram_reel",
                "url": url,
                "status": "error",
                "error": str(item.get("error")),
                "text": "",
                "data": item,
            }

        transcript_text = _extract_primary_text(item if isinstance(item, dict) else {})

        payload: Dict[str, Any] = {
            "platform": "instagram_reel",
            "url": url,
            "status": item.get("status", "success") if isinstance(item, dict) else "success",
            "text": transcript_text,
            "data": item,
        }

        if not transcript_text:
            payload["error"] = "Video transcript actor did not provide transcript text."

        return payload

    return {
        "platform": "instagram_reel",
        "url": url,
        "status": "error",
        "error": "Video transcript actor returned an empty dataset.",
        "text": "",
    }

