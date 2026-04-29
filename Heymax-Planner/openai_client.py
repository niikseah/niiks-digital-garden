"""OpenAI client for generating HeyMax trip plans."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None  # type: ignore

load_dotenv()

ALLOWED_MODELS = {"gpt-4o", "gpt-4o-mini"}
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
MOCK_MODE = os.getenv("OPENAI_MOCK_MODE", "false").lower() == "true"


@dataclass
class PlannerConfig:
    """Runtime configuration for the planner."""

    model: str = DEFAULT_MODEL
    temperature: float = float(os.getenv("OPENAI_TEMPERATURE", "0.6"))
    max_output_tokens: int = int(os.getenv("OPENAI_MAX_OUTPUT_TOKENS", "900"))
    top_p: float = float(os.getenv("OPENAI_TOP_P", "0.9"))

    def __post_init__(self) -> None:
        if self.model not in ALLOWED_MODELS:
            raise ValueError(
                f"OPENAI_MODEL must be one of {sorted(ALLOWED_MODELS)}; got '{self.model}'"
            )
        if not (0 <= self.temperature <= 1.5):
            raise ValueError("OPENAI_TEMPERATURE must be between 0 and 1.5")
        if not (100 <= self.max_output_tokens <= 4000):
            raise ValueError("OPENAI_MAX_OUTPUT_TOKENS must be between 100 and 4000")
        if not (0 < self.top_p <= 1):
            raise ValueError("OPENAI_TOP_P must be in (0, 1]")


class OpenAIPlanner:
    """Wrapper around OpenAI Responses API tailored for HeyMax trip planning."""

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        config: Optional[PlannerConfig] = None,
        mock_mode: Optional[bool] = None,
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.mock_mode = MOCK_MODE if mock_mode is None else mock_mode
        self.config = config or PlannerConfig()

        if not self.mock_mode:
            if not self.api_key:
                raise RuntimeError("OPENAI_API_KEY is missing from environment variables")
            if OpenAI is None:
                raise ImportError(
                    "openai package is not installed. Add 'openai' to dependencies."
                )
            self.client = OpenAI(api_key=self.api_key, default_headers={"X-HeyMax-Use": "trip-planner"})
        else:
            self.client = None

    def call_planner(self, inputs: Dict[str, Any]) -> str:
        """Generate a trip plan from structured inputs."""
        if self.mock_mode:
            return self._mock_response(inputs)

        prompt_payload = build_prompt(inputs)

        try:
            response = self.client.responses.create(  # type: ignore[union-attr]
                model=self.config.model,
                input=[
                    {
                        "role": "system",
                        "content": (
                            "You are HeyMax Trip Planning AI. "
                            "You MUST format your response EXACTLY as specified in the user prompt. "
                            "ONLY output 4 sections: Summary, Accommodation, Things we want to do, and Links. "
                            "DO NOT create day-by-day itineraries, trip snapshots, or other sections. "
                            "Extract specific places, prices, and activities from the inspiration content. "
                            "Use actual names, prices, and details mentioned in the videos/posts. "
                            "Cite inspiration sources using (Inspo #n) format when relevant."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt_payload,
                    },
                ],
                temperature=self.config.temperature,
                top_p=self.config.top_p,
                max_output_tokens=self.config.max_output_tokens,
                metadata={"project": "heymax-trip-planner"},
            )
        except Exception as exc:  # pragma: no cover - network errors
            raise RuntimeError(f"OpenAI API error: {exc}") from exc

        text = extract_text_from_response(response)
        if not text:
            raise RuntimeError("OpenAI API returned an empty response")
        return text

    def _mock_response(self, inputs: Dict[str, Any]) -> str:
        """Generate a lightweight mock response for local testing."""
        trip_context = inputs.get("trip_context", {})
        city = trip_context.get("city", "your destination")
        duration = trip_context.get("duration_days") or "a few"
        start_date = trip_context.get("start_date") or "soon"
        budget = trip_context.get("budget", "flexible")

        return (
            f"# ✨ Preview Plan for {city}\n"
            f"**Dates:** starting {start_date} · **Duration:** {duration} days · **Budget:** {budget}\n\n"
            "## Day 1 – Arrival & Neighborhood Walk\n"
            "- Settle into lodging, grab a local coffee, and scout the area.\n"
            "- Evening: casual dinner plus a stroll guided by your saved clips.\n\n"
            "## Day 2 – Anchor Experiences\n"
            "- Morning landmark visit inspired by your top video.\n"
            "- Afternoon food crawl or museum stop depending on mood.\n"
            "- Nightlife or rooftop rec pulled from social inspiration.\n\n"
            "## Day 3 – Flex & Departure\n"
            "- Buffer for spontaneous finds, shopping, or a day trip.\n"
            "- Wrap with a memorable meal before heading home.\n\n"
            "_Mock mode is enabled. Disable OPENAI_MOCK_MODE to call the real model._"
        )


def format_planner_payload(
    trip_context: Dict[str, Any], extracted_links: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Normalize payload passed to the planner."""
    return {
        "trip_context": trip_context,
        "extracted_links": extracted_links,
    }


def build_prompt(inputs: Dict[str, Any]) -> str:
    """Create a structured prompt with trip context and inspiration insights."""
    trip_context = inputs.get("trip_context", {})
    extracted_links = inputs.get("extracted_links", [])

    context_section = _format_trip_context(trip_context)
    inspiration_section = _format_inspiration_section(extracted_links)

    requirements = (
        "### Deliverable - CRITICAL: Follow this EXACT format, do NOT use day-by-day itineraries\n\n"
        "You MUST produce ONLY the following 4 sections in this exact order:\n\n"
        "1. **Summary:**\n"
        "   - **Flight:** [airline and price if mentioned, otherwise 'TBD']\n"
        "   - **Dates/Times:** [departure and return dates/times]\n\n"
        "2. 🏠 **Accommodation**\n"
        "   - **Option 1:** [description, price]\n"
        "   - **Option 2:** [description, price]\n"
        "   - **Option 3:** [description, price]\n"
        "   - **Option 4:** [description, price]\n"
        "   (Include 2-4 accommodation options with descriptions and prices from the inspiration)\n\n"
        "3. 🏃 **Things we want to do**\n"
        "   - **attractions:**\n"
        "     - [list specific attractions]\n"
        "   - **food / drinks:**\n"
        "     - [list food/drink spots]\n"
        "   - **shopping/ sightseeing:**\n"
        "     - [list shopping/sightseeing spots]\n\n"
        "4. **Links:**\n"
        "   - [List relevant inspiration links as clickable markdown links]\n\n"
        "IMPORTANT RULES:\n"
        "- DO NOT create day-by-day itineraries\n"
        "- DO NOT include 'Trip Snapshot', 'Reservations & Logistics', 'Budget Intel', or 'Local Intel' sections\n"
        "- ONLY use the 4 sections listed above: Summary, Accommodation, Things we want to do, Links\n"
        "- Extract specific places, prices, and activities from the inspiration content\n"
        "- Use actual names, prices, and details mentioned in the videos/posts\n"
        "- Keep descriptions concise and practical\n"
        "- Cite inspiration sources when relevant using (Inspo #n) format\n"
        "- Format accommodation options with clear descriptions and prices\n"
        "- Use actual emoji characters (🏠 and 🏃) in the section headers"
    )

    return f"{context_section}\n\n{inspiration_section}\n\n{requirements}"


def _format_trip_context(trip_context: Dict[str, Any]) -> str:
    """Render trip context as Markdown."""
    lines = ["### Trip Context"]
    lines.append(f"- Destination: {trip_context.get('city') or 'Unknown'}")
    lines.append(f"- Start date: {trip_context.get('start_date') or 'Unspecified'}")
    lines.append(f"- Duration (days): {trip_context.get('duration_days') or 'Unspecified'}")
    lines.append(f"- Group size: {trip_context.get('group_size') or 'Unspecified'}")
    lines.append(f"- Budget: {trip_context.get('budget') or 'Unspecified'}")

    # Additional custom fields if present
    for key, value in trip_context.items():
        if key in {"city", "start_date", "duration_days", "group_size", "budget"}:
            continue
        lines.append(f"- {key.replace('_', ' ').title()}: {value}")
    return "\n".join(lines)


def _format_inspiration_section(
    extracted_links: List[Dict[str, Any]], max_entries: int = 12, max_chars: int = 600
) -> str:
    """Transform extracted link transcripts into a compact reference list."""
    lines = ["### Inspiration Set"]
    if not extracted_links:
        lines.append("- No inspiration links were processed.")
        return "\n".join(lines)

    truncated = 0
    for idx, record in enumerate(extracted_links, start=1):
        if idx > max_entries:
            truncated += 1
            continue

        link = record.get("link", {})
        platform = (link.get("platform") or "unknown").title()
        url = link.get("url", "")
        metadata = link.get("metadata") or {}
        author = metadata.get("author") or metadata.get("channel") or "Unknown author"
        transcript = (link.get("transcript") or "").strip()

        if not transcript:
            snippet = "No transcript captured—use general knowledge."
        else:
            snippet = transcript.replace("\n", " ").strip()
            if len(snippet) > max_chars:
                snippet = snippet[: max_chars - 3].rsplit(" ", 1)[0] + "..."

        lines.append(f"**Inspo #{idx} — {platform} by {author}**")
        if url:
            lines.append(f"- URL: {url}")
        lines.append(f"- Key takeaways: {snippet}")

    if truncated:
        lines.append(f"...plus {truncated} more links (omitted for brevity).")

    lines.append(
        "\nAlways cite inspiration as `(Inspo #n)` when it directly influences a recommendation."
    )
    return "\n".join(lines)


def extract_text_from_response(response: Any) -> str:
    """Safely extract text content from OpenAI responses.create payload."""
    if not response:
        return ""

    # responses.create returns an object with .output list
    try:
        segments = []
        for output in getattr(response, "output", []):
            for content in getattr(output, "content", []):
                text = getattr(content, "text", None)
                if text:
                    segments.append(text)
        return "\n".join(segments).strip()
    except Exception:  # pragma: no cover - defensive
        # fallback for dict-like responses
        choices = getattr(response, "choices", None) or response.get("choices") if isinstance(response, dict) else None
        if choices:
            return choices[0]["message"]["content"]
        return ""


