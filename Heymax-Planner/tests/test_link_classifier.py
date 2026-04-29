"""Tests for link classification functionality."""

import pytest
from utils.link_classifier import classify_link, is_allowed_platform


class TestClassifyLink:
    """Test classify_link() function."""

    def test_youtube_standard_url(self):
        """Test standard YouTube watch URL."""
        url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
        assert classify_link(url) == "youtube"

    def test_youtube_short_url(self):
        """Test YouTube short URL (youtu.be)."""
        url = "https://youtu.be/jNQXAC9IVRw"
        assert classify_link(url) == "youtube"

    def test_youtube_embed_url(self):
        """Test YouTube embed URL."""
        url = "https://www.youtube.com/embed/jNQXAC9IVRw"
        assert classify_link(url) == "youtube"

    def test_youtube_shorts_url(self):
        """Test YouTube Shorts URL."""
        url = "https://www.youtube.com/shorts/ABC123"
        assert classify_link(url) == "youtube"

    def test_youtube_mobile_url(self):
        """Test YouTube mobile URL."""
        url = "https://m.youtube.com/watch?v=jNQXAC9IVRw"
        assert classify_link(url) == "youtube"

    def test_youtube_without_www(self):
        """Test YouTube URL without www."""
        url = "https://youtube.com/watch?v=jNQXAC9IVRw"
        assert classify_link(url) == "youtube"

    def test_youtube_with_http(self):
        """Test YouTube URL with http (not https)."""
        url = "http://www.youtube.com/watch?v=jNQXAC9IVRw"
        assert classify_link(url) == "youtube"

    def test_youtube_with_params(self):
        """Test YouTube URL with additional parameters."""
        url = "https://www.youtube.com/watch?v=jNQXAC9IVRw&t=30s&feature=share"
        assert classify_link(url) == "youtube"

    def test_instagram_post_url(self):
        """Test Instagram post URL."""
        url = "https://www.instagram.com/p/ABC123/"
        assert classify_link(url) == "instagram"

    def test_instagram_reel_url(self):
        """Test Instagram reel URL."""
        url = "https://www.instagram.com/reel/ABC123/"
        assert classify_link(url) == "instagram"

    def test_instagram_reels_url(self):
        """Test Instagram reels URL (plural form)."""
        url = "https://www.instagram.com/reels/ABC123/"
        assert classify_link(url) == "instagram"

    def test_instagram_tv_url(self):
        """Test Instagram TV URL."""
        url = "https://www.instagram.com/tv/ABC123/"
        assert classify_link(url) == "instagram"

    def test_instagram_stories_url(self):
        """Test Instagram stories URL."""
        url = "https://www.instagram.com/stories/user/123456/"
        assert classify_link(url) == "instagram"

    def test_instagram_short_url(self):
        """Test Instagram short URL (instagr.am)."""
        url = "https://instagr.am/p/ABC123/"
        assert classify_link(url) == "instagram"

    def test_instagram_without_www(self):
        """Test Instagram URL without www."""
        url = "https://instagram.com/reel/ABC123/"
        assert classify_link(url) == "instagram"

    def test_tiktok_standard_url(self):
        """Test standard TikTok URL."""
        url = "https://www.tiktok.com/@user/video/1234567890"
        assert classify_link(url) == "tiktok"

    def test_tiktok_short_url(self):
        """Test TikTok short URL (vm.tiktok.com)."""
        url = "https://vm.tiktok.com/ABC123/"
        assert classify_link(url) == "tiktok"

    def test_tiktok_t_url(self):
        """Test TikTok t/ URL format."""
        url = "https://www.tiktok.com/t/ABC123/"
        assert classify_link(url) == "tiktok"

    def test_tiktok_v_url(self):
        """Test TikTok v/ URL format."""
        url = "https://www.tiktok.com/v/1234567890"
        assert classify_link(url) == "tiktok"

    def test_airbnb_rooms_url(self):
        """Test Airbnb rooms URL."""
        url = "https://www.airbnb.com/rooms/12345678"
        assert classify_link(url) == "airbnb"

    def test_airbnb_search_url(self):
        """Test Airbnb search URL."""
        url = "https://www.airbnb.com/s/singapore"
        assert classify_link(url) == "airbnb"

    def test_airbnb_experiences_url(self):
        """Test Airbnb experiences URL."""
        url = "https://www.airbnb.com/experiences/123"
        assert classify_link(url) == "airbnb"

    def test_airbnb_country_domain(self):
        """Test Airbnb with country-specific domain."""
        url = "https://www.airbnb.co.uk/rooms/12345678"
        assert classify_link(url) == "airbnb"

    def test_airbnb_without_www(self):
        """Test Airbnb URL without www."""
        url = "https://airbnb.com/rooms/12345678"
        assert classify_link(url) == "airbnb"

    def test_unknown_platform(self):
        """Test URL from unknown platform."""
        url = "https://example.com/video/123"
        assert classify_link(url) == "unknown"

    def test_facebook_url(self):
        """Test Facebook URL (not supported)."""
        url = "https://facebook.com/video/123"
        assert classify_link(url) == "unknown"

    def test_twitter_url(self):
        """Test Twitter/X URL (not supported)."""
        url = "https://twitter.com/user/status/123"
        assert classify_link(url) == "unknown"

    def test_invalid_url(self):
        """Test invalid URL format."""
        url = "not-a-url"
        assert classify_link(url) == "unknown"

    def test_empty_string(self):
        """Test empty string."""
        url = ""
        assert classify_link(url) == "unknown"

    def test_url_with_fragment(self):
        """Test URL with fragment identifier."""
        url = "https://www.youtube.com/watch?v=jNQXAC9IVRw#t=30s"
        assert classify_link(url) == "youtube"

    def test_url_case_insensitive(self):
        """Test that URL classification is case-insensitive."""
        url = "https://WWW.YOUTUBE.COM/WATCH?V=jNQXAC9IVRw"
        assert classify_link(url) == "youtube"

    def test_url_with_at_prefix(self):
        """Test URL with @ prefix (common in Telegram)."""
        url = "@https://www.youtube.com/watch?v=jNQXAC9IVRw"
        assert classify_link(url) == "youtube"


class TestIsAllowedPlatform:
    """Test is_allowed_platform() function."""

    def test_youtube_allowed(self):
        """Test YouTube is allowed."""
        url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
        assert is_allowed_platform(url) is True

    def test_instagram_allowed(self):
        """Test Instagram is allowed."""
        url = "https://www.instagram.com/reel/ABC123/"
        assert is_allowed_platform(url) is True

    def test_tiktok_allowed(self):
        """Test TikTok is allowed."""
        url = "https://www.tiktok.com/@user/video/123"
        assert is_allowed_platform(url) is True

    def test_airbnb_allowed(self):
        """Test Airbnb is allowed."""
        url = "https://www.airbnb.com/rooms/12345678"
        assert is_allowed_platform(url) is True

    def test_facebook_not_allowed(self):
        """Test Facebook is not allowed."""
        url = "https://facebook.com/video/123"
        assert is_allowed_platform(url) is False

    def test_unknown_not_allowed(self):
        """Test unknown platform is not allowed."""
        url = "https://example.com"
        assert is_allowed_platform(url) is False

    def test_invalid_url_not_allowed(self):
        """Test invalid URL is not allowed."""
        url = "not-a-url"
        assert is_allowed_platform(url) is False

