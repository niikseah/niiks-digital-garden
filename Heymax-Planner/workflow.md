# Technical Workflow Documentation

This document describes the technical architecture, data flow, and implementation details of the HeyMax Trip Planner Bot.

## 🏗️ Architecture Overview

```
User (Telegram) → Bot Handler → State Management → Data Processing → External APIs → Response
                                      ↓
                                 Supabase (Persistence)
```

## 📊 Data Flow

### 1. Trip Context Collection Flow

```
/start command
  ↓
Load existing data from Supabase (if exists)
  ↓
If no data: Start context collection
  ↓
For each question (date, duration, budget, group_size, city):
  ↓
Validate input → Store in chat_data → Ask next question
  ↓
After all questions:
  ↓
Build payload → Save to Supabase → Show summary with buttons
```

### 2. Link Collection Flow

```
User sends message with links
  ↓
Extract URLs using regex
  ↓
Classify each URL (YouTube, Instagram, TikTok, Airbnb, Unknown)
  ↓
Filter allowed platforms only
  ↓
If valid platform:
  ↓
Add to chat_data["links"] → Save to Supabase → Silent acknowledgment
```

### 3. Trip Processing Flow

```
/plan command → User confirms
  ↓
Check if links exist (if 0, show error)
  ↓
Group links by platform
  ↓
For each platform:
  ↓
  Run extractor:
    - YouTube: youtube-transcript-api
    - Instagram: Apify agentx/video-transcript
    - TikTok: Apify clockworks/tiktok-scraper
  ↓
  Extract transcript (no video download)
  ↓
Build link payload with metadata
  ↓
Combine all extracted data
  ↓
Format payload for OpenAI planner:
  {
    "trip_context": {...},
    "extracted_links": [...]
  }
  ↓
Call OpenAI API (or mock)
  ↓
Save results to output.json
  ↓
Update Supabase with trip data
  ↓
Send formatted response to user
```

## 🔧 Component Details

### Bot State Management

The bot uses `context.chat_data` to maintain state:

```python
{
  "idx": 0,  # Current question index
  "trip": {
    "start_date": None,
    "duration_days": None,
    "budget": None,
    "group_size": None,
    "city": None,
  },
  "final_payload": {...},  # Complete trip payload
  "links": [...],  # List of collected links
  "state": "idle",  # idle, collecting_context, collecting_links, removing_links
  "updating_field": None,  # Track which field is being updated
}
```

### Link Classification

The `link_classifier.py` module classifies URLs:

- **YouTube**: Matches `youtube.com`, `youtu.be` patterns
- **Instagram**: Matches `instagram.com/reel`, `instagram.com/p`, etc.
- **TikTok**: Matches `tiktok.com/@user/video/` patterns
- **Airbnb**: Matches `airbnb.com/rooms/`, `airbnb.com/s/`, etc.
- **Unknown**: Everything else

Only links classified as allowed platforms are collected.

### Content Extraction

#### YouTube Extraction
- Uses `youtube-transcript-api` library
- Direct API call to YouTube
- Returns transcript text and metadata

#### Instagram Extraction
- Uses Apify actor: `agentx/video-transcript`
- Input: `video_url`, `target_lang`
- Output: Transcript text from video
- **No video download** - transcript only

#### TikTok Extraction
- Uses Apify actor: `clockworks/tiktok-scraper`
- Input: `postURLs`, `shouldDownloadVideos: False`, `shouldDownloadSubtitles: True`
- Output: Transcript from subtitles or VTT file
- **No video download** - only subtitles/transcripts

### OpenAI Integration

#### Mock Mode
- Generates formatted markdown response locally
- Includes trip context summary and placeholder itinerary
- Avoids spending tokens during development

#### Production Mode
- Uses the OpenAI Responses API with GPT-4o/GPT-4o-mini
- Input: structured JSON with trip context + extracted inspiration snippets
- Output: Markdown-formatted trip plan featuring citations to inspiration links
- `OPENAI_MAX_OUTPUT_TOKENS` keeps responses within budget

### Supabase Integration

#### Tables

**`user_answers`**
- Stores trip context per chat
- Primary key: `chat_id`
- Fields: `start_date`, `duration`, `budget`, `city`, `group_size`, `json_trip_data`

**`links`**
- Stores collected links per chat
- Composite primary key: `(chat_id, link)`
- Prevents duplicate links

#### Operations

- **`load_user_data(chat_id)`**: Load trip context and links
- **`update_database(update, payload, json_data)`**: Upsert trip context
- **`update_single_field(chat_id, field, value)`**: Update only one field
- **`add_link(chat_id, links)`**: Add links (upsert, prevents duplicates)
- **`remove_link_database(chat_id, link)`**: Remove specific link

## 🔄 State Transitions

```
idle
  ↓ /start
collecting_context
  ↓ (all questions answered)
idle (with final_payload)
  ↓ /plan
collecting_links
  ↓ (user confirms)
idle (processing)
  ↓ (extraction complete)
idle (with results)
```

## 📦 Data Structures

### Trip Payload
```python
{
  "user_id": str,
  "chat_id": str,
  "trip": {
    "start_date": str,  # ISO format
    "duration_days": int,
    "budget": str,
    "group_size": int,
    "city": str,
  },
  "meta": {
    "timestamp": str,  # ISO format
    "version": "v1",
    "mode": "group" | "dm",
  }
}
```

### Link Payload (for planner)
```python
{
  "link": {
    "platform": str,  # youtube, instagram, tiktok, airbnb
    "url": str,
    "transcript": str,
    "metadata": {
      "author": str | None,
      "createdTime": str | None,  # ISO format
    },
    "status": str,  # success, error, skipped
    "error": str | None,
  }
}
```

### Planner Input Format
```python
{
  "trip_context": {
    "start_date": str,
    "duration_days": int,
    "budget": str,
    "group_size": int,
    "city": str,
  },
  "extracted_links": [
    {
      "link": {
        "platform": str,
        "url": str,
        "transcript": str,
        "metadata": {...},
      }
    },
    ...
  ]
}
```

## 🛡️ Error Handling

### Validation Errors
- Date: Must be future date in YYYY-MM-DD format
- Duration: Must be positive integer
- Budget: Any text (no validation)
- Group Size: Must be positive integer
- City: Any text (normalized to title case)

### Extraction Errors
- Failed extractions marked with `status: "error"`
- Error message stored in `error` field
- Processing continues with successful extractions
- User notified if all extractions fail

### Database Errors
- Graceful degradation if Supabase unavailable
- Warnings logged but bot continues
- Local state maintained in `chat_data`

## 🔍 Logging and Debugging

### Output Files
- `output.json`: Complete extraction results and trip context
  - Generated on each trip processing
  - Includes all extracted transcripts
  - Summary statistics by platform and status

### Console Logging
- Extraction progress for each platform
- Apify actor run IDs and status
- Database operation results
- Error messages with stack traces

## 🚀 Performance Considerations

### Link Collection
- Silent background collection
- No blocking operations
- Immediate user feedback

### Content Extraction
- Sequential processing (one platform at a time)
- Apify actors run asynchronously on Apify's infrastructure
- YouTube extraction is synchronous but fast
- Total time: ~30-60 seconds for multiple links

### Database Operations
- Upsert operations prevent duplicates
- Single field updates use `.update()` for efficiency
- Batch link operations use bulk upsert

## 🔐 Security Considerations

### Environment Variables
- All sensitive data in `.env` (gitignored)
- No hardcoded credentials
- Service role key for Supabase (read/write access)

### Input Validation
- URL validation before processing
- Platform whitelist prevents malicious links
- Input sanitization for user text

### API Security
- Apify token required for Instagram/TikTok
- OpenAI API key required for planner (keep private; HeyMax use only)
- All API calls use HTTPS

## 📈 Scalability

### Current Limitations
- Sequential link processing
- Single bot instance per token
- In-memory state (lost on restart, but Supabase persists)

### Future Improvements
- Parallel link extraction
- Webhook support for high traffic
- Redis for distributed state management
- Queue system for batch processing

---

**Last Updated**: Current implementation as of latest changes

