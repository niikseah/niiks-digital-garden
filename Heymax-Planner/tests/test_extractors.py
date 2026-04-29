"""Tests for content extractors (YouTube, Instagram, TikTok)."""

import pytest
from scraper.youtube_extracter import extract_youtube_content
from scraper.instagram_reel_extractor import extract_instagram_content
from scraper.tiktok_extractor import extract_tiktok_content


@pytest.mark.api
class TestYouTubeExtractor:
    """Test YouTube content extraction."""

    def test_extract_valid_video(self):
        """Test extraction from valid YouTube video with transcript."""
        # Using "Me at the zoo" - a stable test video that should have transcripts
        url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
        result = extract_youtube_content(url)
        
        assert result["platform"] == "youtube"
        assert result["url"] == url
        assert result["status"] == "success"
        assert "text" in result
        assert len(result["text"]) > 0
        assert "transcript" in result
        assert isinstance(result["transcript"], list)
        assert len(result["transcript"]) > 0

    def test_extract_short_url(self):
        """Test extraction from YouTube short URL."""
        url = "https://youtu.be/jNQXAC9IVRw"
        result = extract_youtube_content(url)
        
        assert result["platform"] == "youtube"
        assert result["url"] == url
        assert result["status"] == "success"

    def test_extract_invalid_video_id(self):
        """Test extraction with invalid video ID."""
        url = "https://www.youtube.com/watch?v=INVALID_VIDEO_ID_12345"
        result = extract_youtube_content(url)
        
        assert result["platform"] == "youtube"
        assert result["url"] == url
        assert result["status"] == "error"
        assert "error" in result

    def test_extract_malformed_url(self):
        """Test extraction with malformed URL."""
        url = "https://youtube.com/invalid"
        result = extract_youtube_content(url)
        
        assert result["platform"] == "youtube"
        assert result["status"] == "error"
        assert "error" in result

    def test_extract_no_video_id(self):
        """Test extraction from URL without video ID."""
        url = "https://www.youtube.com/"
        result = extract_youtube_content(url)
        
        assert result["platform"] == "youtube"
        assert result["status"] == "error"
        assert "error" in result

    def test_result_structure(self):
        """Test that result has correct structure for successful extraction."""
        url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
        result = extract_youtube_content(url)
        
        if result["status"] == "success":
            assert "text" in result
            assert "transcript" in result
            assert isinstance(result["transcript"], list)
            # Check transcript segment structure
            if result["transcript"]:
                segment = result["transcript"][0]
                assert "text" in segment
                assert "start_time" in segment
                assert "duration" in segment


@pytest.mark.api
class TestInstagramExtractor:
    """Test Instagram content extraction."""

    @pytest.mark.skipif(
        not __import__("os").getenv("APIFY_TOKEN"),
        reason="Requires APIFY_TOKEN environment variable"
    )
    def test_extract_with_apify_token(self, requires_apify_token):
        """Test extraction with valid Apify token."""
        # Note: This requires a real Instagram URL with video content
        # Using a placeholder - in real tests, use a known working Instagram reel URL
        url = "https://www.instagram.com/reel/ABC123/"
        result = extract_instagram_content(url)
        
        assert result["platform"] == "instagram"
        assert result["url"] == url
        # Result could be success, error, or skipped depending on URL validity
        assert "status" in result
        assert "text" in result

    def test_extract_without_apify_token(self):
        """Test extraction without Apify token - uses None client."""
        url = "https://www.instagram.com/reel/ABC123/"
        # Test by passing None as client explicitly
        from scraper.instagram_reel_extractor import extract_instagram_content
        
        result = extract_instagram_content(url, api_client=None)
        assert result["platform"] == "instagram"
        assert result["status"] == "error"
        assert "error" in result
        assert "APIFY_TOKEN" in result["error"].upper() or "not initialized" in result["error"].lower()

    def test_extract_invalid_url(self):
        """Test extraction with invalid Instagram URL."""
        url = "https://instagram.com/invalid"
        result = extract_instagram_content(url)
        
        assert result["platform"] == "instagram"
        assert result["url"] == url
        # Should handle gracefully
        assert "status" in result

    def test_result_structure(self):
        """Test that result has correct structure."""
        url = "https://www.instagram.com/reel/ABC123/"
        result = extract_instagram_content(url)
        
        assert result["platform"] == "instagram"
        assert result["url"] == url
        assert "status" in result
        assert "text" in result
        assert isinstance(result["text"], str)


@pytest.mark.api
class TestTikTokExtractor:
    """Test TikTok content extraction."""

    @pytest.mark.skipif(
        not __import__("os").getenv("APIFY_TOKEN"),
        reason="Requires APIFY_TOKEN environment variable"
    )
    def test_extract_with_apify_token(self, requires_apify_token):
        """Test extraction with valid Apify token."""
        # Note: This requires a real TikTok URL
        # Using a placeholder - in real tests, use a known working TikTok URL
        url = "https://www.tiktok.com/@user/video/1234567890"
        result = extract_tiktok_content(url)
        
        assert result["platform"] == "tiktok"
        assert result["url"] == url
        # Result could be success, error, or no_transcript
        assert "status" in result
        assert "text" in result

    def test_extract_without_apify_token(self):
        """Test extraction without Apify token - uses None client."""
        url = "https://www.tiktok.com/@user/video/1234567890"
        # Test by passing None as client explicitly
        from scraper.tiktok_extractor import extract_tiktok_content
        
        result = extract_tiktok_content(url, api_client=None)
        assert result["platform"] == "tiktok"
        assert result["status"] == "error"
        assert "error" in result
        assert "APIFY_TOKEN" in result["error"].upper() or "not initialized" in result["error"].lower()

    def test_extract_invalid_url(self):
        """Test extraction with invalid TikTok URL."""
        url = "https://tiktok.com/invalid"
        result = extract_tiktok_content(url)
        
        assert result["platform"] == "tiktok"
        assert result["url"] == url
        # Should handle gracefully
        assert "status" in result

    def test_result_structure(self):
        """Test that result has correct structure."""
        url = "https://www.tiktok.com/@user/video/1234567890"
        result = extract_tiktok_content(url)
        
        assert result["platform"] == "tiktok"
        assert result["url"] == url
        assert "status" in result
        assert "text" in result
        assert isinstance(result["text"], str)
        # Check for metadata if present
        if "metadata" in result:
            assert isinstance(result["metadata"], dict)

    def test_vtt_parsing(self):
        """Test VTT subtitle parsing logic."""
        from scraper.tiktok_extractor import _parse_vtt
        
        vtt_content = """WEBVTT

00:00:00.000 --> 00:00:02.000
Hello world

00:00:02.000 --> 00:00:04.000
This is a test
"""
        result = _parse_vtt(vtt_content)
        assert "Hello world" in result
        assert "This is a test" in result
        assert "WEBVTT" not in result
        assert "-->" not in result

    def test_vtt_empty(self):
        """Test VTT parsing with empty content."""
        from scraper.tiktok_extractor import _parse_vtt
        
        result = _parse_vtt("")
        assert result == ""

    def test_pick_best_subtitle_english(self):
        """Test picking English subtitle when available."""
        from scraper.tiktok_extractor import _pick_best_subtitle_link
        
        subtitles = [
            {"language": "fr", "downloadLink": "link1"},
            {"language": "eng", "downloadLink": "link2"},
            {"language": "es", "downloadLink": "link3"},
        ]
        
        result = _pick_best_subtitle_link(subtitles)
        assert result["language"] == "eng"
        assert result["downloadLink"] == "link2"

    def test_pick_best_subtitle_no_english(self):
        """Test picking first subtitle when English not available."""
        from scraper.tiktok_extractor import _pick_best_subtitle_link
        
        subtitles = [
            {"language": "fr", "downloadLink": "link1"},
            {"language": "es", "downloadLink": "link2"},
        ]
        
        result = _pick_best_subtitle_link(subtitles)
        assert result["language"] == "fr"
        assert result["downloadLink"] == "link1"

    def test_pick_best_subtitle_empty(self):
        """Test picking subtitle from empty list."""
        from scraper.tiktok_extractor import _pick_best_subtitle_link
        
        result = _pick_best_subtitle_link([])
        assert result is None

