"""
What this does:
- Uses dummy JSON now, but can call Team A's endpoint later.
- Extracts the locations array from the JSON payload.
- Validates required fields.
- Cleans/formats the location objects for Member 2's Leaflet map.
- Handles common errors: malformed JSON, missing keys, empty list, invalid items.

Expected Team A endpoint later:
    /api/trips/{trip_id}/locations

Usage examples:
    python location_parser.py --use-dummy
    python location_parser.py --use-dummy --pretty
    python location_parser.py --trip-id trip_9382 --base-url http://localhost:5000
    python location_parser.py --file dummy_locations.json --pretty
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from urllib.parse import parse_qs, urlparse

#for debugging
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class LocationParserError(Exception):
    """Base exception for parsing/validation errors."""


class MalformedJSONError(LocationParserError):
    """Raised when JSON cannot be parsed."""


class MissingLocationsError(LocationParserError):
    """Raised when the 'locations' field is missing or invalid."""


class EmptyLocationsError(LocationParserError):
    """Raised when the 'locations' list is empty."""

#dummy location 
DEFAULT_DUMMY_PATH = Path(__file__).with_name("dummy_locations.json")


REQUIRED_FIELDS = ["name", "lat", "lng"]
OPTIONAL_FIELDS = ["category", "address", "opening_hours", "phone", "website"]

def extract_trip_id_from_url(url: str) -> str:
    """Extract trip_id from a URL query string.

    Example:
        http://localhost:3000/map?trip_id=trip_9382
    """
    if not url:
        raise ValueError("URL is required")

    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    trip_id = query_params.get("trip_id", [""])[0].strip()

    if not trip_id:
        raise ValueError("Missing trip_id in URL parameters")

    return trip_id

#load JSON and return as dict 
def get_dummy_data(file_path: Optional[str] = None) -> Dict[str, Any]:
    """Load dummy JSON from file.

    Args:
        file_path: Optional custom path to dummy JSON file.

    Returns:
        Parsed JSON dictionary.
    """
    path = Path(file_path) if file_path else DEFAULT_DUMMY_PATH
    logger.info("Loading dummy data from %s", path)

    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Dummy JSON file not found: {path}") from exc

    return parse_json_text(text, source=str(path))


#fetch from Team A's endpoint 
def fetch_from_api(trip_id: str, base_url: str, timeout: int = 10) -> Dict[str, Any]:
    """Fetch live data from Team A's endpoint.

    Args:
        trip_id: Trip identifier.
        base_url: Base API URL, for example 'http://localhost:5000'.
        timeout: Request timeout in seconds.

    Returns:
        Parsed JSON dictionary.
    """
    if not trip_id:
        raise ValueError("trip_id is required for API fetch")
    if not base_url:
        raise ValueError("base_url is required for API fetch")

    url = f"{base_url.rstrip('/')}/api/trips/{trip_id}/locations"
    logger.info("Fetching Team A API: %s", url)

    try:
        with urlopen(url, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
    except HTTPError as exc:
        raise ConnectionError(f"API returned HTTP {exc.code} for {url}") from exc
    except URLError as exc:
        raise ConnectionError(f"API unavailable or unreachable: {exc.reason}") from exc

    return parse_json_text(raw, source=url)



def parse_json_text(text: str, source: str = "input") -> Dict[str, Any]:
    """Parse JSON text into a dictionary."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise MalformedJSONError(f"Malformed JSON from {source}: {exc}") from exc

    if not isinstance(data, dict):
        raise MalformedJSONError(f"Top-level JSON from {source} must be an object")

    return data



def parse_locations(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract locations list from payload."""
    if "locations" not in data:
        raise MissingLocationsError("Missing 'locations' field in payload")

    locations = data["locations"]
    if not isinstance(locations, list):
        raise MissingLocationsError("'locations' must be a list")

    if len(locations) == 0:
        raise EmptyLocationsError("'locations' list is empty")

    return locations



def _to_float(value: Any, field_name: str) -> float:
    """Convert numeric input to float, or raise ValueError."""
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Field '{field_name}' must be numeric") from exc



def validate_and_clean_location(loc: Dict[str, Any], index: int = 0) -> Dict[str, Any]:
    """Validate one location object and return a cleaned version.

    Required fields:
    - name
    - lat
    - lng

    Optional fields are included as empty strings if missing.
    """
    if not isinstance(loc, dict):
        raise ValueError(f"Location at index {index} must be an object")

    missing_required = [field for field in REQUIRED_FIELDS if field not in loc or loc[field] in (None, "")]
    if missing_required:
        raise ValueError(f"Location at index {index} missing required fields: {', '.join(missing_required)}")

    cleaned: Dict[str, Any] = {
        "name": str(loc["name"]).strip(),
        "lat": _to_float(loc["lat"], "lat"),
        "lng": _to_float(loc["lng"], "lng"),
        "category": str(loc.get("category", "")).strip(),
        "address": str(loc.get("address", "")).strip(),
        "opening_hours": str(loc.get("opening_hours", "")).strip(),
        "phone": str(loc.get("phone", "")).strip(),
        "website": str(loc.get("website", "")).strip(),
    }

    if not cleaned["name"]:
        raise ValueError(f"Location at index {index} has empty 'name'")

    if not (-90 <= cleaned["lat"] <= 90):
        raise ValueError(f"Location at index {index} has invalid latitude")
    if not (-180 <= cleaned["lng"] <= 180):
        raise ValueError(f"Location at index {index} has invalid longitude")

    return cleaned



def format_locations(locations: List[Dict[str, Any]], skip_invalid: bool = True) -> List[Dict[str, Any]]:
    """Validate and format all locations for Leaflet.

    Args:
        locations: Raw location list.
        skip_invalid: If True, bad locations are skipped. If False, the first bad
            location raises an exception.

    Returns:
        Cleaned location list.
    """
    cleaned_locations: List[Dict[str, Any]] = []
    errors: List[str] = []

    for index, loc in enumerate(locations):
        try:
            cleaned_locations.append(validate_and_clean_location(loc, index=index))
        except ValueError as exc:
            message = str(exc)
            if skip_invalid:
                logger.warning("Skipping invalid location: %s", message)
                errors.append(message)
            else:
                raise

    if not cleaned_locations:
        if errors:
            raise EmptyLocationsError("No valid locations after validation")
        raise EmptyLocationsError("No locations available after formatting")

    return cleaned_locations



def build_output_payload(data: Dict[str, Any], cleaned_locations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Build final payload for downstream map rendering."""
    return {
        "trip_id": str(data.get("trip_id", "")),
        "locations": cleaned_locations,
    }



def get_clean_locations(
    use_dummy: bool = True,
    trip_id: str = "",
    base_url: str = "",
    file_path: Optional[str] = None,
    skip_invalid: bool = True,
) -> Dict[str, Any]:
    """Main entry point.

    Returns:
        A payload with trip_id and cleaned locations.
    """
    if use_dummy:
        data = get_dummy_data(file_path=file_path)
    else:
        data = fetch_from_api(trip_id=trip_id, base_url=base_url)

    raw_locations = parse_locations(data)
    cleaned_locations = format_locations(raw_locations, skip_invalid=skip_invalid)
    return build_output_payload(data, cleaned_locations)



def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Parse and clean location data for Leaflet integration.")
    source_group = parser.add_mutually_exclusive_group()
    source_group.add_argument("--use-dummy", action="store_true", help="Use dummy JSON data (default if no source is given)")
    source_group.add_argument("--file", type=str, help="Load JSON from a specific local file")
    source_group.add_argument("--api", action="store_true", help="Fetch from Team A API")

    parser.add_argument("--trip-id", type=str, default="trip_9382", help="Trip ID for API fetch")
    parser.add_argument("--base-url", type=str, default="", help="Base URL for Team A API, e.g. http://localhost:5000")
    parser.add_argument("--url", type=str, default="", help="Page URL containing trip_id query parameter, e.g. http://localhost:3000/map?trip_id=trip_9382",)
    parser.add_argument("--strict", action="store_true", help="Do not skip invalid locations")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()

    # Default behavior: use dummy JSON if no explicit source is selected.
    use_dummy = (not args.api and not args.file) or args.use_dummy

    trip_id = args.trip_id
    if args.url:
        trip_id = extract_trip_id_from_url(args.url)
        logger.info("Extracted trip_id from URL: %s", trip_id)

    try:
        payload = (
            get_clean_locations(
                use_dummy=use_dummy and not bool(args.file),
                trip_id=trip_id,
                base_url=args.base_url,
                file_path=args.file if args.file else None,
                skip_invalid=not args.strict,
            )
            if not args.file
            else _load_from_file_and_process(args.file, skip_invalid=not args.strict)
        )
    except (LocationParserError, ConnectionError, FileNotFoundError, ValueError) as exc:
        logger.error(str(exc))
        return 1

    if args.pretty:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(payload, ensure_ascii=False))
    return 0



def _load_from_file_and_process(file_path: str, skip_invalid: bool = True) -> Dict[str, Any]:
    """Load from arbitrary local JSON file and process it."""
    data = get_dummy_data(file_path=file_path)
    raw_locations = parse_locations(data)
    cleaned_locations = format_locations(raw_locations, skip_invalid=skip_invalid)
    return build_output_payload(data, cleaned_locations)


if __name__ == "__main__":
    sys.exit(main())
