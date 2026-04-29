# User Flow Documentation

This document describes the user experience and interaction flow of the HeyMax Trip Planner Bot from a user's perspective.

## 🎯 Overview

The bot provides a friendly, conversational experience for planning trips. It minimizes typing and uses buttons for most interactions, making it feel like chatting with a friend rather than filling out forms.

## 🚀 Getting Started

### First Time User

```
User: /start
  ↓
Bot: Welcome message with "Let's go! 🚀" button
  ↓
User: Clicks "Let's go! 🚀"
  ↓
Bot: "When is your trip? (YYYY-MM-DD)"
  ↓
User: "2025-12-25"
  ↓
Bot: "How many days?"
  ↓
User: "7"
  ↓
Bot: "What's your budget?"
  ↓
User: "$2000"
  ↓
Bot: "How many people?"
  ↓
User: "2"
  ↓
Bot: "Where are you going?"
  ↓
User: "Paris"
  ↓
Bot: Shows trip summary with "✅ Add Details" and "✏️ Update Details" buttons
  ↓
User: Clicks "✅ Add Details"
  ↓
Bot: Confirms trip details saved, shows next steps (press /plan, add links)
```

### Returning User

```
User: /start
  ↓
Bot: "👋 Welcome back! I found your previous trip data:"
     Shows existing trip summary
     Buttons: "✏️ Update Details", "📎 Manage Links", "🆕 Start Fresh"
  ↓
User: Can choose to:
  - Update details
  - Manage links
  - Start fresh
```

## 📋 Main Flows

### 1. Trip Context Collection Flow

**Entry Point**: `/start`

**Steps**:
1. Bot asks: "When is your trip? (YYYY-MM-DD)"
2. User enters date → Bot validates (must be future date)
3. Bot asks: "How many days?"
4. User enters number → Bot validates (must be positive)
5. Bot asks: "What's your budget?"
6. User enters text → No validation
7. Bot asks: "How many people?"
8. User enters number → Bot validates (must be positive)
9. Bot asks: "Where are you going?"
10. User enters city → Bot normalizes to title case
11. Bot shows summary with confirmation buttons

**Error Handling**:
- Invalid date: "❌ Please enter a future date. Your trip date should be in the future!"
- Invalid duration: "❌ Please send a positive number of days (e.g., 5)"
- Invalid group size: "❌ Please enter a valid group size (1 or more people)"
- Bot shows error and asks again for the same question

**Completion**:
- User clicks "✅ Add Details" → Trip saved, shows next steps
- User clicks "✏️ Update Details" → Goes to update menu

### 2. Link Collection Flow

**Entry Point**: `/plan` or sending links directly

**Via `/plan` command**:
```
User: /plan
  ↓
Bot: If links exist, shows them with pagination
     If no links: "📎 Send me links from YouTube, Instagram, TikTok, or Airbnb..."
  ↓
User: Sends links in messages
  ↓
Bot: Silently collects valid links (no response)
     Ignores invalid links (no response)
```

**Direct Link Sending**:
```
User: Sends message with links
  ↓
Bot: Extracts URLs from message
  ↓
Bot: Classifies each URL
  ↓
Bot: If valid platform (YouTube, Instagram, TikTok, Airbnb):
       - Adds to collection silently
       - Saves to database
     If invalid:
       - Ignores silently
```

**Link Management**:
```
User: /links
  ↓
Bot: Shows links (10 per page) with:
     - Page navigation (◀️ Previous, Next ▶️)
     - "🗑️ Remove Links" button
  ↓
User: Clicks "🗑️ Remove Links"
  ↓
Bot: Shows links again with format examples:
     "Enter link numbers to remove:
      Examples: 1, 1,3,5, 1-5, 1,3-5,7"
  ↓
User: Enters "1,3,5" or "1-5" or "1,3-5,7"
  ↓
Bot: Removes specified links
     Shows updated list
```

**Link Removal Formats**:
- Single: `1`
- Multiple: `1,3,5`
- Range: `1-5`
- Mixed: `1,3-5,7`

### 3. Trip Planning Flow

**Entry Point**: `/plan` (after links are collected)

```
User: /plan
  ↓
Bot: Shows collected links (if any)
     User can remove links if needed
  ↓
User: Ready to plan (has links)
  ↓
Bot: "⏳ Processing your links and creating your trip plan... This might take a moment!"
  ↓
Bot: (Background processing)
     - Extracts transcripts from links
     - Groups by platform
    - Calls OpenAI planner (or mock)
     - Saves to output.json
  ↓
Bot: "✨ Your Personalized Trip Plan:"
     Shows formatted markdown response
```

**Error Cases**:
- No links: "❌ Too little information to plan a trip! I need at least some inspiration links..."
- Extraction fails: Continues with successful extractions, shows warning if needed

### 4. Update Flow

**Entry Point**: `/update` or "✏️ Update Details" button

```
User: /update
  ↓
Bot: Shows current trip details with buttons:
     - "📅 Update Date"
     - "⏱️ Update Duration"
     - "💰 Update Budget"
     - "👥 Update Group Size"
     - "🌍 Update City"
     - "✅ Done"
  ↓
User: Clicks "🌍 Update City"
  ↓
Bot: "Where are you going?"
  ↓
User: "Tokyo"
  ↓
Bot: "✅ City updated!"
     Shows update menu again (with updated city)
```

**Key Feature**: Only the selected field is updated in the database, other fields remain unchanged.

## 🎨 User Experience Features

### Friendly Messages
- Uses emojis for visual appeal
- Conversational tone ("Let's go! 🚀", "Perfect! ✅")
- Clear instructions with examples
- Helpful error messages

### Button-Based Interactions
- Minimal typing required
- Clear action buttons
- Inline keyboards for quick actions
- Pagination for long lists

### Silent Operations
- Links collected in background
- No interruption for link collection
- Smooth, non-intrusive experience

### Session Persistence
- Data saved automatically
- Resumes from where you left off
- No need to re-enter information

## 📱 Command Reference

### `/start`
- **Purpose**: Begin or resume trip planning
- **Behavior**: 
  - If no data: Start context collection
  - If data exists: Show existing data with options
- **Buttons**: "Let's go! 🚀" or "✏️ Update Details", "📎 Manage Links", "🆕 Start Fresh"

### `/plan`
- **Purpose**: Collect links and process trip
- **Behavior**:
  - Shows existing links if any
  - Switches to link collection mode
  - Processes trip when user is ready
- **Note**: Only processes if links exist

### `/links`
- **Purpose**: View and manage collected links
- **Behavior**:
  - Shows links with pagination (10 per page)
  - Allows removal by number/range
- **Buttons**: "🗑️ Remove Links", pagination buttons

### `/update`
- **Purpose**: Update trip details
- **Behavior**:
  - Shows current values
  - Allows updating individual fields
  - Only updates the selected field
- **Buttons**: Field-specific update buttons, "✅ Done"

### `/help`
- **Purpose**: Show help information
- **Behavior**: Lists all commands and how to use them

### `/cancel`
- **Purpose**: Cancel current operation
- **Behavior**: Returns to idle state, clears current operation

## 🔄 State Management

### User States

**Idle**
- Bot is waiting for commands
- Can send links (collected silently)
- Can use any command

**Collecting Context**
- Bot is asking trip questions
- User must answer current question
- Can use `/cancel` to abort

**Collecting Links**
- Bot is ready to collect links
- User can send links
- Links collected silently

**Removing Links**
- Bot is waiting for link numbers to remove
- User enters numbers in specified format
- Can use `/cancel` to abort

**Processing**
- Bot is extracting content and calling the OpenAI planner
- User should wait
- No interaction needed

## 💡 Best Practices for Users

### Efficient Link Collection
1. Send multiple links in one message (all collected)
2. Use `/links` to verify collected links
3. Remove unwanted links before planning

### Updating Details
1. Use `/update` to change specific fields
2. No need to re-enter all information
3. Changes saved immediately

### Planning Tips
1. Collect at least a few links before planning
2. Mix different platforms (YouTube, Instagram, TikTok)
3. Add Airbnb links for accommodation ideas
4. Review links before processing

## 🎯 User Goals

### Primary Goal
Plan a personalized trip based on:
- Trip context (date, duration, budget, group size, city)
- Inspiration links (videos, posts, listings)

### Secondary Goals
- Save trip details for later
- Update trip details easily
- Manage collected links
- Get AI-generated trip plan

## 🚨 Error Scenarios

### Invalid Input
- **Date**: User enters past date or wrong format
  - Bot: Shows error, asks again
- **Duration**: User enters negative number or text
  - Bot: Shows error, asks again
- **Group Size**: User enters 0 or negative
  - Bot: Shows error, asks again

### Missing Data
- **No links when planning**: Bot shows helpful message
- **No trip context**: Bot prompts to use `/start`

### Network Issues
- **Apify failure**: Extraction marked as error, continues with others
- **OpenAI failure**: User notified, can retry
- **Supabase failure**: Bot continues with local state, warns user

## 📊 Example Conversations

### Complete Flow Example

```
User: /start
Bot: 👋 Welcome! I'm HeyMax Trip Planner Bot...
     [Let's go! 🚀]

User: [Clicks button]
Bot: When is your trip? (YYYY-MM-DD)

User: 2025-12-25
Bot: How many days?

User: 7
Bot: What's your budget?

User: $2000
Bot: How many people?

User: 2
Bot: Where are you going?

User: Paris
Bot: 🎉 Great! Here's what I've got:
     📅 Date: 2025-12-25
     ⏱️ Duration: 7 days
     💰 Budget: $2000
     👥 Group Size: 2 people
     🌍 City: Paris
     [✅ Add Details] [✏️ Update Details]

User: [Clicks "✅ Add Details"]
Bot: ✅ Perfect! Your trip details are saved.
     📋 Next steps:
     • Press /plan to plan your trip
     • But remember to add your links first! ✨

User: /plan
Bot: 📎 Send me links from YouTube, Instagram, TikTok, or Airbnb...

User: https://www.youtube.com/watch?v=example
Bot: [Silently collects]

User: https://www.instagram.com/reels/example/
Bot: [Silently collects]

User: /links
Bot: 📎 Collected Links (2 total):
     1. https://www.youtube.com/watch?v=example
     2. https://www.instagram.com/reels/example/
     [🗑️ Remove Links]

User: /plan
Bot: ⏳ Processing your links and creating your trip plan...
     [Processing...]
     ✨ Your Personalized Trip Plan:
     [Markdown formatted plan]
```

---

**Designed for a smooth, friendly user experience** 🎉

