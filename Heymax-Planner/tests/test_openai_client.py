"""Tests for OpenAI client functionality."""

import os
import pytest
from openai_client import (
    OpenAIPlanner,
    PlannerConfig,
    format_planner_payload,
    build_prompt,
    _format_trip_context,
    _format_inspiration_section,
)


class TestPlannerConfig:
    """Test PlannerConfig dataclass."""

    def test_valid_config(self):
        """Test creating valid config."""
        config = PlannerConfig(
            model="gpt-4o-mini",
            temperature=0.6,
            max_output_tokens=900,
            top_p=0.9,
        )
        assert config.model == "gpt-4o-mini"
        assert config.temperature == 0.6
        assert config.max_output_tokens == 900
        assert config.top_p == 0.9

    def test_invalid_model(self):
        """Test config with invalid model."""
        with pytest.raises(ValueError, match="OPENAI_MODEL must be one of"):
            PlannerConfig(model="invalid-model")

    def test_invalid_temperature_too_low(self):
        """Test config with temperature below 0."""
        with pytest.raises(ValueError, match="OPENAI_TEMPERATURE must be between"):
            PlannerConfig(temperature=-0.1)

    def test_invalid_temperature_too_high(self):
        """Test config with temperature above 1.5."""
        with pytest.raises(ValueError, match="OPENAI_TEMPERATURE must be between"):
            PlannerConfig(temperature=2.0)

    def test_invalid_max_tokens_too_low(self):
        """Test config with max_output_tokens below 100."""
        with pytest.raises(ValueError, match="OPENAI_MAX_OUTPUT_TOKENS must be between"):
            PlannerConfig(max_output_tokens=50)

    def test_invalid_max_tokens_too_high(self):
        """Test config with max_output_tokens above 4000."""
        with pytest.raises(ValueError, match="OPENAI_MAX_OUTPUT_TOKENS must be between"):
            PlannerConfig(max_output_tokens=5000)

    def test_invalid_top_p_too_low(self):
        """Test config with top_p at or below 0."""
        with pytest.raises(ValueError, match="OPENAI_TOP_P must be in"):
            PlannerConfig(top_p=0.0)

    def test_invalid_top_p_too_high(self):
        """Test config with top_p above 1."""
        with pytest.raises(ValueError, match="OPENAI_TOP_P must be in"):
            PlannerConfig(top_p=1.5)

    def test_valid_boundary_values(self):
        """Test config with boundary values."""
        config = PlannerConfig(
            temperature=0.0,
            max_output_tokens=100,
            top_p=1.0,
        )
        assert config.temperature == 0.0
        assert config.max_output_tokens == 100
        assert config.top_p == 1.0


class TestOpenAIPlanner:
    """Test OpenAIPlanner class."""

    def test_init_with_mock_mode(self):
        """Test initializing planner with mock mode."""
        planner = OpenAIPlanner(mock_mode=True)
        assert planner.mock_mode is True
        assert planner.client is None

    def test_init_without_api_key(self):
        """Test initializing planner without API key (should fail if not mock)."""
        # Temporarily remove API key
        original_key = os.environ.get("OPENAI_API_KEY")
        try:
            if "OPENAI_API_KEY" in os.environ:
                del os.environ["OPENAI_API_KEY"]
            
            # Should work in mock mode
            planner = OpenAIPlanner(mock_mode=True)
            assert planner.mock_mode is True
            
            # Should fail without mock mode
            with pytest.raises(RuntimeError, match="OPENAI_API_KEY is missing"):
                OpenAIPlanner(mock_mode=False)
        finally:
            if original_key:
                os.environ["OPENAI_API_KEY"] = original_key

    @pytest.mark.api
    def test_call_planner_mock_mode(self, sample_trip_data):
        """Test calling planner in mock mode."""
        planner = OpenAIPlanner(mock_mode=True)
        inputs = format_planner_payload(sample_trip_data, [])
        result = planner.call_planner(inputs)
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert "Mock mode" in result or "Preview Plan" in result

    @pytest.mark.api
    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY"),
        reason="Requires OPENAI_API_KEY environment variable"
    )
    def test_call_planner_real_api(self, sample_trip_data, requires_openai_key):
        """Test calling planner with real OpenAI API."""
        planner = OpenAIPlanner(mock_mode=False)
        inputs = format_planner_payload(sample_trip_data, [])
        result = planner.call_planner(inputs)
        
        assert isinstance(result, str)
        assert len(result) > 0
        # Real API should return actual content, not mock message
        assert "Mock mode" not in result

    @pytest.mark.api
    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY"),
        reason="Requires OPENAI_API_KEY environment variable"
    )
    def test_call_planner_with_extracted_links(self, sample_trip_data, requires_openai_key):
        """Test calling planner with extracted links."""
        planner = OpenAIPlanner(mock_mode=False)
        extracted_links = [
            {
                "link": {
                    "platform": "youtube",
                    "url": "https://www.youtube.com/watch?v=test",
                    "transcript": "This is a test transcript about Singapore travel.",
                    "metadata": {"author": "Test Author"},
                }
            }
        ]
        inputs = format_planner_payload(sample_trip_data, extracted_links)
        result = planner.call_planner(inputs)
        
        assert isinstance(result, str)
        assert len(result) > 0


class TestFormatPlannerPayload:
    """Test format_planner_payload() function."""

    def test_format_payload_structure(self, sample_trip_data):
        """Test payload structure."""
        extracted_links = []
        payload = format_planner_payload(sample_trip_data, extracted_links)
        
        assert "trip_context" in payload
        assert "extracted_links" in payload
        assert payload["trip_context"] == sample_trip_data
        assert payload["extracted_links"] == extracted_links

    def test_format_payload_with_links(self, sample_trip_data):
        """Test payload with extracted links."""
        extracted_links = [
            {"link": {"platform": "youtube", "url": "test", "transcript": "test"}}
        ]
        payload = format_planner_payload(sample_trip_data, extracted_links)
        
        assert len(payload["extracted_links"]) == 1
        assert payload["extracted_links"] == extracted_links


class TestBuildPrompt:
    """Test build_prompt() function."""

    def test_build_prompt_structure(self, sample_trip_data):
        """Test prompt structure."""
        extracted_links = []
        inputs = format_planner_payload(sample_trip_data, extracted_links)
        prompt = build_prompt(inputs)
        
        assert "Trip Context" in prompt
        assert "Inspiration Set" in prompt
        assert "Deliverable" in prompt
        assert sample_trip_data["city"] in prompt

    def test_build_prompt_with_links(self, sample_trip_data):
        """Test prompt with extracted links."""
        extracted_links = [
            {
                "link": {
                    "platform": "youtube",
                    "url": "https://www.youtube.com/watch?v=test",
                    "transcript": "Test transcript content",
                    "metadata": {"author": "Test Author"},
                }
            }
        ]
        inputs = format_planner_payload(sample_trip_data, extracted_links)
        prompt = build_prompt(inputs)
        
        assert "Inspiration Set" in prompt
        assert "youtube" in prompt.lower()
        assert "Test transcript" in prompt


class TestFormatTripContext:
    """Test _format_trip_context() function."""

    def test_format_complete_context(self, sample_trip_data):
        """Test formatting complete trip context."""
        result = _format_trip_context(sample_trip_data)
        
        assert "Trip Context" in result
        assert sample_trip_data["city"] in result
        assert sample_trip_data["start_date"] in result
        assert str(sample_trip_data["duration_days"]) in result
        assert str(sample_trip_data["group_size"]) in result
        assert sample_trip_data["budget"] in result

    def test_format_partial_context(self):
        """Test formatting partial trip context."""
        partial_data = {
            "city": "Singapore",
            "start_date": "2025-12-25",
        }
        result = _format_trip_context(partial_data)
        
        assert "Singapore" in result
        assert "2025-12-25" in result
        assert "Unspecified" in result  # For missing fields

    def test_format_empty_context(self):
        """Test formatting empty context."""
        result = _format_trip_context({})
        
        assert "Trip Context" in result
        assert "Unknown" in result or "Unspecified" in result


class TestFormatInspirationSection:
    """Test _format_inspiration_section() function."""

    def test_format_empty_links(self):
        """Test formatting with no links."""
        result = _format_inspiration_section([])
        
        assert "Inspiration Set" in result
        assert "No inspiration links" in result

    def test_format_single_link(self):
        """Test formatting with single link."""
        extracted_links = [
            {
                "link": {
                    "platform": "youtube",
                    "url": "https://www.youtube.com/watch?v=test",
                    "transcript": "This is a test transcript about travel.",
                    "metadata": {"author": "Test Author"},
                }
            }
        ]
        result = _format_inspiration_section(extracted_links)
        
        assert "Inspiration Set" in result
        assert "Inspo #1" in result
        assert "youtube" in result.lower()
        assert "Test Author" in result
        assert "test transcript" in result.lower()

    def test_format_multiple_links(self):
        """Test formatting with multiple links."""
        extracted_links = [
            {
                "link": {
                    "platform": "youtube",
                    "url": "https://www.youtube.com/watch?v=test1",
                    "transcript": "First transcript",
                    "metadata": {"author": "Author1"},
                }
            },
            {
                "link": {
                    "platform": "instagram",
                    "url": "https://www.instagram.com/reel/test2",
                    "transcript": "Second transcript",
                    "metadata": {"author": "Author2"},
                }
            },
        ]
        result = _format_inspiration_section(extracted_links)
        
        assert "Inspo #1" in result
        assert "Inspo #2" in result
        assert "youtube" in result.lower()
        assert "instagram" in result.lower()

    def test_format_link_without_transcript(self):
        """Test formatting link without transcript."""
        extracted_links = [
            {
                "link": {
                    "platform": "youtube",
                    "url": "https://www.youtube.com/watch?v=test",
                    "transcript": "",
                    "metadata": {},
                }
            }
        ]
        result = _format_inspiration_section(extracted_links)
        
        assert "No transcript captured" in result

    def test_format_link_truncation(self):
        """Test that long transcripts are truncated."""
        long_transcript = " ".join(["word"] * 1000)  # Very long transcript
        extracted_links = [
            {
                "link": {
                    "platform": "youtube",
                    "url": "https://www.youtube.com/watch?v=test",
                    "transcript": long_transcript,
                    "metadata": {},
                }
            }
        ]
        result = _format_inspiration_section(extracted_links, max_chars=100)
        
        assert len(result) < len(long_transcript)
        assert "..." in result

    def test_format_max_entries_limit(self):
        """Test that only max_entries links are included."""
        extracted_links = [
            {
                "link": {
                    "platform": "youtube",
                    "url": f"https://www.youtube.com/watch?v=test{i}",
                    "transcript": f"Transcript {i}",
                    "metadata": {},
                }
            }
            for i in range(15)  # More than default max_entries (12)
        ]
        result = _format_inspiration_section(extracted_links, max_entries=12)
        
        assert "Inspo #12" in result
        assert "plus 3 more links" in result  # 15 - 12 = 3

