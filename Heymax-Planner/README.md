# HeyMax Trip Planner Bot

A friendly Telegram bot that helps users plan amazing trips by collecting trip details, gathering inspiration links from YouTube, Instagram, TikTok, and Airbnb, extracting transcripts, and generating personalized trip plans using OpenAI GPT-4o models.

## 🌟 Features

- 🎯 **Interactive Trip Planning**: Collect trip details through friendly Q&A
- 🔗 **Silent Link Collection**: Automatically collects links from messages in the background
- 📎 **Smart Link Management**: View and manage collected links with pagination and easy removal
- 🎬 **Multi-Platform Content Extraction**: Extracts transcripts from YouTube, Instagram, and TikTok videos
- 🤖 **AI-Powered Planning**: Generates personalized trip plans via GPT-4o / GPT-4o-mini
- 💾 **Data Persistence**: Stores trip data and links in Supabase for session continuity
- 🎨 **Button-Based UX**: Minimal typing required, friendly conversational interface
- ✏️ **Flexible Updates**: Update individual trip details without re-entering everything

## 📋 Requirements

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) or `pip`
- Telegram Bot Token ([Get one from @BotFather](https://t.me/BotFather))
- Apify API Token (for Instagram/TikTok extraction)
- OpenAI API key (GPT-4o or GPT-4o-mini; mock mode available for testing)
- Supabase URL and Service Role Key

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd heymax-trip-planner
pip install -e .
```

Or with uv:

```bash
uv sync
```

### 2. Configure Environment

Create a `.env` file in the project root:

```env
# Telegram Bot Token
BOT_TOKEN=your_telegram_bot_token

# Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

# Apify Token (for Instagram/TikTok extraction)
APIFY_TOKEN=your_apify_token

# OpenAI Planner Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini  # Allowed: gpt-4o or gpt-4o-mini
OPENAI_MOCK_MODE=true     # Set false to call OpenAI
OPENAI_MAX_OUTPUT_TOKENS=900
```

### 3. Set Up Supabase Tables

Create the following tables in your Supabase project:

**`user_answers` table:**
```sql
CREATE TABLE user_answers (
  chat_id BIGINT PRIMARY KEY,
  user_id BIGINT,
  start_date TEXT,
  duration INTEGER,
  budget TEXT,
  city TEXT,
  group_size INTEGER,
  json_trip_data JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

**`links` table:**
```sql
CREATE TABLE links (
  chat_id BIGINT,
  link TEXT,
  PRIMARY KEY (chat_id, link),
  created_at TIMESTAMP DEFAULT NOW()
);
```

### 4. Run the Bot

```bash
python bot.py
```

You should see:
```
🤖 HeyMax Trip Planner Bot is running...
```

## 📖 Usage

### Commands

- `/start` - Begin setting up your trip details or view existing data
- `/plan` - Start collecting inspiration links and process your trip
- `/links` - View and manage your collected links (with pagination)
- `/confirm` - Send the latest trip summary back to the chat
- `/update` - Update your trip details (individual fields)
- `/help` - Show help message
- `/cancel` - Cancel current operation

### How It Works

1. **Trip Context Collection** (`/start`)
   - User answers questions about their trip
   - Trip date (YYYY-MM-DD format)
   - Duration (number of days)
   - Budget (free text)
   - Group size (number of people)
   - Destination city
   - Data is saved to Supabase automatically

2. **Link Collection** (`/plan`)
   - User sends links from YouTube, Instagram, TikTok, or Airbnb
   - Links are collected silently in the background
   - Only valid platform links are accepted
   - Invalid links are ignored silently
   - Use `/links` to view and manage collected links

3. **Content Extraction** (when processing trip)
   - YouTube videos: Transcripts extracted via `youtube-transcript-api`
   - Instagram Reels: Transcripts extracted via Apify actor (transcript only, no video download)
   - TikTok videos: Transcripts extracted via Apify actor (transcript only, no video download)
   - Airbnb links: Stored but no transcript extraction

4. **AI Planning** (`/plan` → Process)
   - Extracted content and trip context are formatted and sent to the OpenAI planner prompt
   - In mock mode: Generates formatted test response without API usage
   - In production: Calls GPT-4o or GPT-4o-mini via the OpenAI Responses API
   - Results are saved to `output.json` for debugging

5. **Personalized Plan**
   - User receives a markdown-formatted trip plan
   - All data is persisted to Supabase

## 📁 Project Structure

```
heymax-trip-planner/
├── bot.py                    # Main bot file with all handlers
├── openai_client.py          # OpenAI planner client (with mock mode)
├── supa.py                   # Supabase integration
├── pyproject.toml            # Dependencies and project config
├── README.md                 # This file
├── workflow.md               # Technical workflow documentation
├── userflow.md               # User experience flow documentation
├── scraper/                  # Content extractors
│   ├── __init__.py
│   ├── youtube_extracter.py  # YouTube transcript extraction
│   ├── instagram_extractor.py # Instagram transcript extraction (Apify)
│   └── tiktok_extractor.py   # TikTok transcript extraction (Apify)
└── utils/                    # Utility functions
    ├── __init__.py
    ├── workflow.py           # Data extraction workflow orchestration
    ├── link_classifier.py    # Link classification and validation
    └── apify_client_config.py # Apify client configuration
```

## 🎬 Supported Platforms

- ✅ **YouTube** - Full transcript extraction via `youtube-transcript-api`
- ✅ **Instagram** - Reels, Posts, Stories (via Apify `agentx/video-transcript` actor)
- ✅ **TikTok** - Video transcripts (via Apify `clockworks/tiktok-scraper` actor)
- ✅ **Airbnb** - Link collection (no transcript extraction)

**Note**: Apify extractors are configured to only extract transcripts, not download videos, for efficiency.

## ⚙️ Configuration

### OpenAI Planner

- By default `OPENAI_MOCK_MODE=true`, so no tokens are spent.
- Set `OPENAI_MOCK_MODE=false` once you're ready to call GPT-4o/GPT-4o-mini.
- Supported models: `gpt-4o` (higher quality) and `gpt-4o-mini` (budget-friendly).
- Optional knobs:
  - `OPENAI_TEMPERATURE` (default `0.6`)
  - `OPENAI_TOP_P` (default `0.9`)
  - `OPENAI_MAX_OUTPUT_TOKENS` (default `900` to stay within monthly budget)

Make sure you never share the OpenAI API key publicly and only use it for the HeyMax planner.

### Apify Setup

1. Sign up at [Apify](https://apify.com)
2. Get your API token from [Settings](https://console.apify.com/account/integrations)
3. Add to `.env`:
   ```env
   APIFY_TOKEN=your_apify_token
   ```

## 🔒 Security Notes

- ⚠️ **Never commit `.env` file to version control**
- 🔑 Use service role keys securely
- 🛡️ Keep API tokens private
- 🔐 The bot uses Supabase service role key for database operations
- 🚫 `.env` is already in `.gitignore`

## 🐛 Troubleshooting

### Bot won't start
- Check that `BOT_TOKEN` is set in `.env`
- Verify the token is valid with @BotFather
- Check Python version (requires 3.12+)

### Supabase errors
- Verify `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` are correct
- Check that database tables exist with correct schema
- Ensure service role key has proper permissions
- On local development, architecture mismatch warnings are normal (works in production)

### Link extraction fails
- Check `APIFY_TOKEN` is set (for Instagram/TikTok)
- Verify you have Apify credits
- YouTube extraction works without Apify
- Check Apify actor status

### OpenAI planner errors
- Confirm `OPENAI_MOCK_MODE=false` only when the API key is set
- Ensure `OPENAI_MODEL` is `gpt-4o` or `gpt-4o-mini`
- Check network connectivity and current OpenAI status
- Lower `OPENAI_MAX_OUTPUT_TOKENS` if you see quota/cost errors

## 📚 Documentation

- **[README.md](README.md)** - This file, project overview and setup
- **[workflow.md](workflow.md)** - Technical workflow and architecture
- **[userflow.md](userflow.md)** - User experience and interaction flow

## 🛠️ Development

### Code Structure

- `bot.py` - Main bot logic with command handlers, state management, and user interactions
- `openai_client.py` - GPT-4o integration with prompt builder + mock mode
- `supa.py` - Supabase database operations (CRUD for trip data and links)
- `scraper/` - Platform-specific extractors (YouTube, Instagram, TikTok)
- `utils/` - Shared utilities (link classification, workflow orchestration, Apify config)

### Key Features Implementation

- **Session Persistence**: Data loaded from Supabase on `/start` if exists
- **Single Field Updates**: Only updates the specific field being changed
- **Silent Link Collection**: Links collected in background without interrupting user
- **Pagination**: Links displayed 10 per page with navigation
- **Smart Link Removal**: Remove by number, range, or comma-separated list

## 📝 License

This project is part of the HeyMax AI Itinerary Planner system.

## 🤝 Support

For issues or questions:
1. Check the documentation files (`workflow.md`, `userflow.md`)
2. Verify your `.env` configuration
3. Check Supabase table schemas match requirements
4. Ensure all API tokens are valid and have credits

---

**Built with ❤️ for seamless trip planning**
