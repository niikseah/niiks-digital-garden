import re

# Allowed platforms for link collection
ALLOWED_PLATFORMS = ["youtube", "instagram", "instagram_reel", "instagram_post", "tiktok", "airbnb"]

def classify_link(url: str) -> str:
    """
    Classify a URL to determine if it's from YouTube, Instagram, TikTok, or Airbnb.
    Returns 'unknown' if the platform is not supported.
    
    Args:
        url (str): The URL to classify
        
    Returns:
        str: The platform name ('youtube', 'instagram', 'tiktok', 'airbnb') or 'unknown'
    """
    
    # YouTube patterns
    youtube_patterns = [
        r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/v/)',
        r'(?:https?://)?(?:www\.)?(?:m\.youtube\.com/watch\?v=)',
        r'(?:https?://)?(?:www\.)?(?:youtube\.com/shorts/)'
    ]
    
    # Instagram patterns
    instagram_reel_patterns = [
        r'(?:https?://)?(?:www\.)?instagram\.com/reel/',
        r'(?:https?://)?(?:www\.)?instagram\.com/reels/',  # Plural form
        r'(?:https?://)?(?:www\.)?instagram\.com/tv/',
    ]

    instagram_post_patterns = [
        r'(?:https?://)?(?:www\.)?instagram\.com/p/',
        r'(?:https?://)?(?:www\.)?instagr\.am/p/'
    ]

    instagram_patterns = [
        r'(?:https?://)?(?:www\.)?instagram\.com/stories/',
    ]
    
    # TikTok patterns
    tiktok_patterns = [
        r'(?:https?://)?(?:www\.)?tiktok\.com/@[\w.-]+/video/\d+',
        r'(?:https?://)?(?:vm\.)?tiktok\.com/[\w.-]+',
        r'(?:https?://)?(?:www\.)?tiktok\.com/t/[\w.-]+',
        r'(?:https?://)?(?:www\.)?tiktok\.com/v/\d+'
    ]
    
    # Airbnb patterns
    airbnb_patterns = [
        r'(?:https?://)?(?:www\.)?airbnb\.(?:com|co\.\w+)(?:/rooms/|/s/|/experiences/)',
        r'(?:https?://)?(?:www\.)?airbnb\.com\.\w+/rooms/',
        r'(?:https?://)?(?:www\.)?airbnb\.com\.\w+/s/',
        r'(?:https?://)?(?:www\.)?airbnb\.com\.\w+/experiences/',
    ]
    
    # Check for YouTube
    for pattern in youtube_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            return 'youtube'
    
    # Check for Instagram Reel
    for pattern in instagram_reel_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            return 'instagram_reel'

    # Check for Instagram Post
    for pattern in instagram_post_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            return 'instagram_post'

    # Check for other Instagram
    for pattern in instagram_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            return 'instagram'
    
    # Check for TikTok
    for pattern in tiktok_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            return 'tiktok'
    
    # Check for Airbnb
    for pattern in airbnb_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            return 'airbnb'
    
    return 'unknown'

def is_allowed_platform(url: str) -> bool:
    """
    Check if a URL is from an allowed platform.
    
    Args:
        url (str): The URL to check
        
    Returns:
        bool: True if the URL is from an allowed platform, False otherwise
    """
    platform = classify_link(url)
    return platform in ALLOWED_PLATFORMS

