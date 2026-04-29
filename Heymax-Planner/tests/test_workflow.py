"""Tests for workflow orchestration."""

import pytest
from datetime import datetime
from utils.workflow import (
    process_links_batch,
    build_link_payload,
    extract_metadata_from_result,
    _normalise_created_time,
)


class TestProcessLinksBatch:
    """Test process_links_batch() function."""

    @pytest.mark.api
    def test_process_youtube_links(self):
        """Test processing YouTube links."""
        links_map = {
            "youtube": ["https://www.youtube.com/watch?v=jNQXAC9IVRw"]
        }
        results = process_links_batch(links_map)
        
        assert len(results) == 1
        assert "link" in results[0]
        link_data = results[0]["link"]
        assert link_data["platform"] == "youtube"
        assert link_data["url"] == links_map["youtube"][0]
        assert "transcript" in link_data
        assert "metadata" in link_data

    @pytest.mark.api
    def test_process_mixed_platforms(self):
        """Test processing links from multiple platforms."""
        links_map = {
            "youtube": ["https://www.youtube.com/watch?v=jNQXAC9IVRw"],
            "airbnb": ["https://www.airbnb.com/rooms/12345678"],
        }
        results = process_links_batch(links_map)
        
        assert len(results) == 2
        platforms = [r["link"]["platform"] for r in results]
        assert "youtube" in platforms
        assert "airbnb" in platforms

    def test_process_empty_links(self):
        """Test processing empty links map."""
        links_map = {}
        results = process_links_batch(links_map)
        
        assert results == []

    def test_process_unknown_platform(self):
        """Test processing unknown platform (should skip)."""
        links_map = {
            "unknown": ["https://example.com"]
        }
        results = process_links_batch(links_map)
        
        assert len(results) == 1
        assert results[0]["link"]["platform"] == "unknown"
        assert results[0]["link"]["status"] == "skipped"

    @pytest.mark.api
    def test_process_multiple_same_platform(self):
        """Test processing multiple links from same platform."""
        links_map = {
            "youtube": [
                "https://www.youtube.com/watch?v=jNQXAC9IVRw",
                "https://youtu.be/jNQXAC9IVRw",  # Same video, different URL format
            ]
        }
        results = process_links_batch(links_map)
        
        assert len(results) == 2
        assert all(r["link"]["platform"] == "youtube" for r in results)

    def test_process_airbnb_links(self):
        """Test processing Airbnb links (no extraction)."""
        links_map = {
            "airbnb": ["https://www.airbnb.com/rooms/12345678"]
        }
        results = process_links_batch(links_map)
        
        assert len(results) == 1
        assert results[0]["link"]["platform"] == "airbnb"
        assert results[0]["link"]["status"] == "skipped"


class TestBuildLinkPayload:
    """Test build_link_payload() function."""

    def test_build_payload_success(self):
        """Test building payload from successful extraction."""
        result = {
            "platform": "youtube",
            "url": "https://www.youtube.com/watch?v=test",
            "text": "This is a test transcript",
            "status": "success",
            "metadata": {
                "author": "Test Author",
                "createdTime": "2025-01-01T00:00:00Z",
            },
        }
        payload = build_link_payload(result)
        
        assert "link" in payload
        link = payload["link"]
        assert link["platform"] == "youtube"
        assert link["url"] == result["url"]
        assert link["transcript"] == result["text"]
        assert link["status"] == "success"
        assert link["metadata"]["author"] == "Test Author"
        assert link["metadata"]["createdTime"] == "2025-01-01T00:00:00.000Z"  # Normalized format

    def test_build_payload_with_error(self):
        """Test building payload from failed extraction."""
        result = {
            "platform": "youtube",
            "url": "https://www.youtube.com/watch?v=invalid",
            "status": "error",
            "error": "Video not found",
        }
        payload = build_link_payload(result)
        
        assert payload["link"]["status"] == "error"
        assert payload["link"]["error"] == "Video not found"
        assert payload["link"]["transcript"] == ""

    def test_build_payload_empty_metadata(self):
        """Test building payload with empty metadata."""
        result = {
            "platform": "youtube",
            "url": "https://www.youtube.com/watch?v=test",
            "text": "Test transcript",
            "status": "success",
        }
        payload = build_link_payload(result)
        
        assert payload["link"]["metadata"] == {}

    def test_build_payload_no_text(self):
        """Test building payload with no transcript text."""
        result = {
            "platform": "youtube",
            "url": "https://www.youtube.com/watch?v=test",
            "status": "success",
        }
        payload = build_link_payload(result)
        
        assert payload["link"]["transcript"] == ""

    def test_build_payload_non_string_text(self):
        """Test building payload with non-string text."""
        result = {
            "platform": "youtube",
            "url": "https://www.youtube.com/watch?v=test",
            "text": 12345,  # Not a string
            "status": "success",
        }
        payload = build_link_payload(result)
        
        assert payload["link"]["transcript"] == ""


class TestExtractMetadata:
    """Test extract_metadata_from_result() function."""

    def test_extract_author_from_metadata(self):
        """Test extracting author from metadata field."""
        result = {
            "metadata": {
                "author": "Test Author",
            }
        }
        metadata = extract_metadata_from_result(result)
        
        assert metadata["author"] == "Test Author"

    def test_extract_author_from_data(self):
        """Test extracting author from data field."""
        result = {
            "data": {
                "author": "Test Author",
            }
        }
        metadata = extract_metadata_from_result(result)
        
        assert metadata["author"] == "Test Author"

    def test_extract_author_variations(self):
        """Test extracting author from various field names."""
        variations = [
            {"author": "Author1"},
            {"authorName": "Author2"},
            {"author_name": "Author3"},
            {"username": "Author4"},
            {"ownerUsername": "Author5"},
            {"channel": "Author6"},
        ]
        
        for var in variations:
            result = {"metadata": var}
            metadata = extract_metadata_from_result(result)
            assert metadata["author"] is not None

    def test_extract_created_time_from_metadata(self):
        """Test extracting created time from metadata."""
        result = {
            "metadata": {
                "createdTime": "2025-01-01T00:00:00Z",
            }
        }
        metadata = extract_metadata_from_result(result)
        
        assert metadata["createdTime"] == "2025-01-01T00:00:00.000Z"

    def test_extract_created_time_variations(self):
        """Test extracting created time from various field names."""
        variations = [
            {"createdTime": "2025-01-01T00:00:00Z"},
            {"createTime": "2025-01-01T00:00:00Z"},
            {"published_at": "2025-01-01T00:00:00Z"},
            {"timestamp": 1735689600},  # Unix timestamp
        ]
        
        for var in variations:
            result = {"metadata": var}
            metadata = extract_metadata_from_result(result)
            if metadata["createdTime"]:
                assert metadata["createdTime"].endswith("Z")

    def test_extract_no_metadata(self):
        """Test extracting from result with no metadata."""
        result = {}
        metadata = extract_metadata_from_result(result)
        
        assert metadata["author"] is None
        assert metadata["createdTime"] is None

    def test_extract_priority_order(self):
        """Test that metadata field takes priority over data field."""
        result = {
            "metadata": {"author": "Metadata Author"},
            "data": {"author": "Data Author"},
        }
        metadata = extract_metadata_from_result(result)
        
        assert metadata["author"] == "Metadata Author"


class TestNormaliseCreatedTime:
    """Test _normalise_created_time() function."""

    def test_normalise_iso_string(self):
        """Test normalizing ISO format string."""
        result = _normalise_created_time("2025-01-01T00:00:00Z")
        assert result == "2025-01-01T00:00:00.000Z"

    def test_normalise_iso_with_fractional(self):
        """Test normalizing ISO string with fractional seconds."""
        result = _normalise_created_time("2025-01-01T00:00:00.123Z")
        assert result == "2025-01-01T00:00:00.000Z"

    def test_normalise_unix_timestamp(self):
        """Test normalizing Unix timestamp."""
        # 2025-01-01 00:00:00 UTC
        timestamp = 1735689600
        result = _normalise_created_time(timestamp)
        assert result is not None
        assert result.endswith("Z")

    def test_normalise_unix_timestamp_float(self):
        """Test normalizing Unix timestamp as float."""
        timestamp = 1735689600.0
        result = _normalise_created_time(timestamp)
        assert result is not None
        assert result.endswith("Z")

    def test_normalise_date_only(self):
        """Test normalizing date-only string."""
        result = _normalise_created_time("2025-01-01")
        assert result == "2025-01-01T00:00:00.000Z"

    def test_normalise_datetime_string(self):
        """Test normalizing datetime string without Z."""
        result = _normalise_created_time("2025-01-01 00:00:00")
        assert result == "2025-01-01T00:00:00.000Z"

    def test_normalise_none(self):
        """Test normalizing None value."""
        result = _normalise_created_time(None)
        assert result is None

    def test_normalise_empty_string(self):
        """Test normalizing empty string."""
        result = _normalise_created_time("")
        assert result is None

    def test_normalise_invalid_format(self):
        """Test normalizing invalid format."""
        result = _normalise_created_time("invalid-date")
        assert result is None

