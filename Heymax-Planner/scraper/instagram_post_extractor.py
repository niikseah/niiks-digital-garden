import cv2
import easyocr
import os
import tempfile
import shutil
import subprocess
import re
import time
from typing import List, Dict, Any
from pathlib import Path

class OCRExtractor:
    _instance = None

    def __init__(self, languages: List[str] = None):
        """Initialize OCR reader with specified languages."""
        if languages is None:
            languages = ['en']  # English by default, add 'ja', 'zh' etc. as needed
        self.reader = easyocr.Reader(languages, gpu=False)  # Set gpu=True if CUDA available
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls(languages=['en'])
        return cls._instance

    @classmethod
    def extract_content(cls, url: str) -> Dict[str, Any]:
        return cls.get_instance().extract_text_from_instagram_post(url)

    def extract_text_from_frame(self, frame) -> str:
        """Extract text from a single frame/image using OCR."""
        results = self.reader.readtext(frame)
        
        # results format: [(bbox, text, confidence), ...]
        texts = [text for (bbox, text, confidence) in results if confidence > 0.3]
        return " ".join(texts)
    
    def extract_text_from_instagram_post(self, url: str) -> Dict:
        """
        Download Instagram post using instaloader CLI and extract text from all images.
        
        Args:
            url: Instagram post URL (e.g., https://www.instagram.com/p/DQWD-nAEl69/)
        
        Returns:
            Dict with extracted text and metadata
        """
        download_dir = None
        
        try:
            print("  📥 Downloading Instagram post...")
            
            # Extract post shortcode from URL
            # URL format: https://www.instagram.com/p/SHORTCODE/ or variants
            shortcode_match = re.search(r'/p/([A-Za-z0-9_-]+)', url)
            if not shortcode_match:
                return {
                    "platform": "instagram_post",
                    "url": url,
                    "status": "error",
                    "error": "Invalid Instagram URL",
                    "text": ""
                }
            
            shortcode = shortcode_match.group(1)
            print(f"  🔍 Post shortcode: {shortcode}")
            download_dir = f'-{shortcode}'
            
            # Use instaloader CLI to download the post
            # instaloader downloads to AppData\Local\Temp\ocr_instagram_* by default
            try:
                cmd = ['instaloader', '--', f'-{shortcode}']
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                if result.returncode != 0:
                    print(f"  ⚠️  instaloader return code: {result.returncode}")
                    print(f"  📝 Output: {result.stderr[:200]}")
            except FileNotFoundError:
                return {
                    "platform": "instagram_post",
                    "url": url,
                    "status": "error",
                    "error": "instaloader not found. Run: pip install instaloader",
                    "text": ""
                }
            except subprocess.TimeoutExpired:
                return {
                    "platform": "instagram_post",
                    "url": url,
                    "status": "error",
                    "error": "Download timeout (30s exceeded)",
                    "text": ""
                }
            
            # Find downloaded image files in the -SHORTCODE directory created by instaloader
            image_files = []
            
            if os.path.exists(download_dir):
                for root, dirs, files in os.walk(download_dir):
                    for f in sorted(files):
                        if f.endswith(('.jpg', '.jpeg', '.png')):
                            full_path = os.path.join(root, f)
                            image_files.append(full_path)
            
            if not image_files:
                return {
                    "platform": "instagram_post",
                    "url": url,
                    "status": "error",
                    "error": "No images found in " + download_dir,
                    "text": ""
                }
            
            print(f"  🖼️  Found {len(image_files)} image(s)")
            print(f"  🔍 Running OCR on images...")
            
            # Run OCR on each image
            all_texts = []
            for idx, img_path in enumerate(image_files):
                try:
                    frame = cv2.imread(img_path)
                    if frame is None:
                        continue
                    
                    text = self.extract_text_from_frame(frame)
                    if text.strip():
                        all_texts.append(text)
                        print(f"    ✓ Extracted from image {idx + 1}")
                except Exception as e:
                    print(f"    ⚠️  Error processing image {idx}: {str(e)[:50]}")
                    continue
            
            combined_text = " ".join(all_texts)
            
            return {
                "platform": "instagram_post",
                "url": url,
                "status": "success",
                "text": combined_text,
                "images_processed": len(image_files),
                "texts_found": len(all_texts)
            }
        
        except Exception as e:
            return {
                "platform": "instagram_post",
                "url": url,
                "status": "error",
                "error": f"Error: {str(e)[:100]}",
                "text": ""
            }
        
        finally:
            # Cleanup downloaded directory
            if download_dir and os.path.exists(download_dir):
                try:
                    shutil.rmtree(download_dir)
                    print(f"  🗑️  Cleaned up: {download_dir}")
                except Exception as e:
                    print(f"  ⚠️  Failed to cleanup {download_dir}: {str(e)[:50]}")

def extract_instagram_post_content(url: str) -> Dict[str, Any]:
    """
    Wrapper function to extract text from an Instagram post.
    
    Args:
        url (str): The Instagram post URL.
        
    Returns:
        Dict[str, Any]: The extraction result.
    """
    return OCRExtractor.extract_content(url)
    
    
if __name__ == "__main__":
    print("🎬 Instagram Post OCR Extractor")
    print("-" * 50)
    
    url = input("Enter Instagram post URL: ").strip()
    
    if not url:
        print("❌ No URL provided.")
        exit(1)
    
    print("\n⏳ Initializing OCR engine (loading language models)...")
    print("   This may take 30-60 seconds on first run...")
    # extractor = OCRExtractor(languages=['en'])
    
    # print("✅ OCR engine ready!")
    print("\n⏳ Processing Instagram post...")
    
    result = OCRExtractor.extract_content(url)
    
    print("\n" + "=" * 50)
    if result.get("status") == "success":
        print("✅ Extraction successful!")
        print(f"\n📝 Extracted Text ({result.get('texts_found', 0)} texts from {result.get('images_processed', 0)} images):")
        print("-" * 50)
        print(result.get("text", ""))
    else:
        print(f"❌ Extraction failed: {result.get('error', 'Unknown error')}")
    print("=" * 50)

