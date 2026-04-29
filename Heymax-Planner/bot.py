"""HeyMax Trip Planner Telegram Bot - Data extraction + OpenAI itinerary generation."""

import os
import re
import json
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any, Tuple
from supa import update_database, add_link, remove_link_database, load_user_data, update_single_field
from utils.link_classifier import classify_link, is_allowed_platform
from utils.workflow import process_links_batch
from openai_client import OpenAIPlanner, format_planner_payload

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN missing in .env")

# Context questions in order
QUESTIONS = ["start_date", "duration", "budget", "group_size", "city"]

# URL regex for extracting links from messages (handles @ prefix and other characters before https)
URL_RE = re.compile(r"(@?https?://[^\s]+)", re.IGNORECASE)

# Question strings
START_DATE_QUESTION = "📅 What's the date of your trip? (YYYY-MM-DD format)"
DURATION_QUESTION = "⏱️ How many days will your trip last? (e.g., 5)"
BUDGET_QUESTION = "💰 What's your budget? (e.g., 2000 SGD or 'mid-range')"
GROUP_SIZE_QUESTION = "👥 How many people are in your group? (e.g., 4)"
DESTINATION_QUESTION = "🌍 Which city are you visiting? (e.g., Singapore)"

# Message strings
WELCOME_MESSAGE = (
    "👋 Hey there! I'm your friendly trip planning assistant.\n\n"
    "Let's get started! I'll ask you a few quick questions about your trip.\n\n"
    "Ready? Let's begin! 🚀"
)

PLAN_MESSAGE = (
    "📋 Great! Now let's collect some inspiration links.\n\n"
    "Just send me links from:\n"
    "• YouTube\n"
    "• Instagram\n"
    "• TikTok\n"
    "• Airbnb\n\n"
    "I'll collect them silently in the background. Use /links to see what you've collected! ✨"
)

EMPTY_DETAILS = "Hmm, I don't have your trip details yet. Use /start to begin! 😊"
SUCCESSFUL_SAVE = "✅ Perfect! Your trip details have been saved."
WRONG_DAYS_FORMAT = "❌ Please send a positive number of days (e.g., 5)"
INVALID_DATE_FORMAT = "❌ Invalid date format. Please use YYYY-MM-DD (e.g., 2025-12-25)"
INVALID_GROUP_SIZE = "❌ Please enter a valid group size (1 or more people)"
PROCESSING_MESSAGE = "⏳ Processing your links and creating your trip plan... This might take a moment!"
EXTRACTION_ERROR = "⚠️ Some links couldn't be processed, but I'll continue with what I have."
NEXT_STEPS = (
    "📋 Next steps:\n"
    "Use /plan to view details and links collected\n"
)


def init_chat_state(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Initialize chat state if not already present."""
    cd = context.chat_data
    cd.setdefault("idx", 0)  # question index
    cd.setdefault("trip", {
        "start_date": None,
        "duration_days": None,
        "budget": None,
        "group_size": None,
        "city": None,
    })
    cd.setdefault("final_payload", None)
    cd.setdefault("links", [])  # list[str]
    cd.setdefault("state", "idle")  # idle, collecting_context, collecting_links
    cd.setdefault("updating_field", None)  # Track which field is being updated (None = not updating)


def to_iso(s: str) -> Optional[str]:
    """Convert date string to ISO format."""
    try:
        dt = datetime.strptime(s.strip(), "%Y-%m-%d")
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return None


def fmt_links(links: List[str]) -> str:
    """Format links list for display."""
    if not links:
        return "No links collected yet. 📭"
    return "\n".join(f"{i+1}. {u}" for i, u in enumerate(links))


def group_links_by_domain(links: List[str]) -> Dict[str, List[str]]:
    """Group links by platform."""
    grouped = {}
    for url in links:
        platform = classify_link(url)
        if platform != "unknown":
            grouped.setdefault(platform, []).append(url)
    return grouped


def build_trip_summary(trip: Dict[str, Any], links: List[str]) -> str:
    """Build a friendly trip summary message."""
    trip_lines = [
        f"📅 **Date:** {trip.get('start_date') or '—'}",
        f"⏱️ **Duration:** {trip.get('duration_days') or '—'} days",
        f"💰 **Budget:** {trip.get('budget') or '—'}",
        f"👥 **Group Size:** {trip.get('group_size') or '—'} people",
        f"🌍 **City:** {trip.get('city') or '—'}",
    ]
    links_text = f"\n📎 **Links collected:** {len(links)}"
    if links:
        links_text += "\n" + "\n".join(f"  • {u}" for u in links[:5])
        if len(links) > 5:
            links_text += f"\n  ... and {len(links) - 5} more"
    
    return "Here's your trip plan:\n\n" + "\n".join(trip_lines) + links_text


def has_trip_data(trip: Dict[str, Any]) -> bool:
    """Return True if any primary trip fields are filled."""
    return any([
        trip.get("start_date"),
        trip.get("duration_days"),
        trip.get("budget"),
        trip.get("city"),
        trip.get("group_size")
    ])


async def send_trip_summary_message(message_obj, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Send trip summary with next steps. Returns True if summary was sent."""
    chat_id = message_obj.chat.id
    trip = context.chat_data.get("trip", {})
    links = context.chat_data.get("links", [])
    
    if not has_trip_data(trip):
        existing_trip, existing_links = load_user_data(chat_id)
        if existing_trip:
            context.chat_data["trip"] = {
                "start_date": existing_trip.get("start_date"),
                "duration_days": existing_trip.get("duration"),
                "budget": existing_trip.get("budget"),
                "group_size": existing_trip.get("group_size"),
                "city": existing_trip.get("city"),
            }
            trip = context.chat_data["trip"]
        if existing_links:
            context.chat_data["links"] = existing_links
            links = existing_links
    
    if not has_trip_data(trip):
        await message_obj.reply_text(
            "I still need your trip details before I can summarize them. Use /start to share them! 😊",
            parse_mode=ParseMode.MARKDOWN
        )
        return False
    
    summary = build_trip_summary(trip, links)
    keyboard_buttons = []
    keyboard_buttons.append([InlineKeyboardButton("✏️ Update Details", callback_data="update_trip")])
    if links:
        keyboard_buttons.append([InlineKeyboardButton("📎 Manage Links", callback_data="view_links")])
        keyboard_buttons.append([InlineKeyboardButton("🚀 Generate summary message", callback_data="confirm_links")])
        
    keyboard_buttons.append([InlineKeyboardButton("🆕 Start Fresh", callback_data="start_fresh")])

    keyboard = InlineKeyboardMarkup(keyboard_buttons)
    
    await message_obj.reply_text(
        f"📝 **Trip summary**\n\n{summary}\n\n" + "➡️Keep the inspiration links coming- I'll silently collect them in the background.",
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )
    return True


# ---------- Command Handlers ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command - begin context collection or use existing data."""
    init_chat_state(context)
    chat_id = update.effective_chat.id
    
    # Try to load existing data from Supabase
    existing_trip, existing_links = load_user_data(chat_id)
    
    # Check if we have existing data
    has_existing_data = existing_trip and any([
        existing_trip.get("start_date"),
        existing_trip.get("duration"),
        existing_trip.get("budget"),
        existing_trip.get("city"),
        existing_trip.get("group_size")
    ])
    
    if has_existing_data or existing_links:
        # Load existing data into chat state
        if existing_trip:
            context.chat_data["trip"] = {
                "start_date": existing_trip.get("start_date"),
                "duration_days": existing_trip.get("duration"),
                "budget": existing_trip.get("budget"),
                "group_size": existing_trip.get("group_size"),
                "city": existing_trip.get("city"),
            }
        if existing_links:
            context.chat_data["links"] = existing_links
        
        # Check if all required fields are filled
        trip = context.chat_data["trip"]
        all_filled = all([
            trip.get("start_date"),
            trip.get("duration_days"),
            trip.get("budget"),
            trip.get("city"),
            trip.get("group_size")
        ])
        
        if all_filled:
            # Rebuild payload
            payload = {
                "user_id": str(update.effective_user.id),
                "chat_id": str(update.effective_chat.id),
                "trip": trip,
                "meta": {
                    "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
                    "version": "v1",
                    "mode": "group" if update.effective_chat.type in ("group", "supergroup") else "dm",
                },
            }
            context.chat_data["final_payload"] = payload
        
        # Show existing data - don't ask to complete, just show options
        # summary = build_trip_summary(trip, existing_links)
        message = "👋 Welcome back! I found your previous trip data:\n\n"
        
        # keyboard_buttons = []
        # # Always show update option (not "complete" - user can update if needed)
        # keyboard_buttons.append([InlineKeyboardButton("✏️ Update Details", callback_data="update_trip")])
        
        # if existing_links:
        #     keyboard_buttons.append([InlineKeyboardButton("📎 Manage Links", callback_data="view_links")])
        
        # keyboard_buttons.append([InlineKeyboardButton("🆕 Start Fresh", callback_data="start_fresh")])
        
        # keyboard = InlineKeyboardMarkup(keyboard_buttons)
        await update.effective_message.reply_text(message)
        
        await send_trip_summary_message(update.effective_message, context)
        
    else:
        # No existing data, start fresh
        context.chat_data["idx"] = 0
        context.chat_data["state"] = "collecting_context"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Let's go! 🚀", callback_data="start_context")]
        ])
        
        await update.message.reply_text(
            WELCOME_MESSAGE,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )

async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /plan command - send trip summary."""
    init_chat_state(context)
    if not update.message:
        return
    await send_trip_summary_message(update.message, context)

# async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Handle /plan command - switch to link collection mode."""
#     init_chat_state(context)
#     chat_id = update.effective_chat.id
    
#     # Load links from Supabase if not in memory
#     links = context.chat_data.get("links", [])
#     if not links:
#         _, existing_links = load_user_data(chat_id)
#         if existing_links:
#             context.chat_data["links"] = existing_links
#             links = existing_links
    
#     context.chat_data["state"] = "collecting_links"
    
#     if links:
#         # Show link summary: number, first 3 links, message about /links, and Start Planning button
#         total_links = len(links)
#         first_three = links[:3]
        
#         message = f"📎 You have {total_links} link{'s' if total_links != 1 else ''} collected:\n\n"
        
#         for i, link in enumerate(first_three, 1):
#             message += f"{i}. {link}\n"
        
#         if total_links > 3:
#             message += f"\n... and {total_links - 3} more link{'s' if total_links - 3 != 1 else ''}\n"
        
#         message += "\n💡 To view all links, use /links\n\n"
#         message += "Ready to create your trip plan?"
        
#         keyboard = InlineKeyboardMarkup([
#             [InlineKeyboardButton("🚀 Start Planning", callback_data="confirm_links")]
#         ])
        
#         await update.message.reply_text(
#             message,
#             reply_markup=keyboard,
#             parse_mode=None  # No markdown to avoid parsing errors with URLs
#         )
#     else:
#         await update.message.reply_text(
#             PLAN_MESSAGE,
#             parse_mode=ParseMode.MARKDOWN
#         )


async def links_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /links command - show collected links with management options."""
    init_chat_state(context)
    chat_id = update.effective_chat.id
    
    # Load links from Supabase if not in memory
    links = context.chat_data.get("links", [])
    if not links:
        _, existing_links = load_user_data(chat_id)
        if existing_links:
            context.chat_data["links"] = existing_links
            links = existing_links
    
    if not links:
        await update.message.reply_text(
            "📭 No links collected yet. Send me some links and I'll collect them! ✨",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    await show_links_with_buttons(update, context, links)


def escape_markdown(text: str) -> str:
    """Escape special markdown characters to prevent parsing errors."""
    # Escape special markdown characters
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text


async def show_remove_links_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE, links: List[str], page: int = 0) -> None:
    """Show paginated links for removal with format examples."""
    LINKS_PER_PAGE = 10
    total_links = len(links)
    total_pages = (total_links + LINKS_PER_PAGE - 1) // LINKS_PER_PAGE
    
    # Get message object
    if update.callback_query:
        message_obj = update.callback_query.message
    else:
        message_obj = update.message
    
    # Calculate pagination
    start_idx = page * LINKS_PER_PAGE
    end_idx = min(start_idx + LINKS_PER_PAGE, total_links)
    page_links = links[start_idx:end_idx]
    
    # Build message - use plain text for links to avoid markdown parsing issues
    message = "🗑️ Remove Links\n\n"
    message += "Enter the link numbers you want to remove:\n\n"
    
    # Show paginated links (plain text, no markdown)
    for i, link in enumerate(page_links, start=start_idx + 1):
        message += f"{i}. {link}\n"
    
    if total_pages > 1:
        message += f"\nPage {page + 1} of {total_pages}\n"
    
    message += "\n📝 Format Examples:\n"
    message += "• Single: 1\n"
    message += "• Multiple: 1,3,5\n"
    message += "• Range: 1-5\n"
    message += "• Mixed: 1,3-5,7\n\n"
    message += "Type /cancel to cancel."
    
    # Create keyboard
    keyboard_buttons = []
    
    # Pagination buttons
    if total_pages > 1:
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("◀️ Previous", callback_data=f"remove_page_{page - 1}"))
        if page < total_pages - 1:
            nav_buttons.append(InlineKeyboardButton("Next ▶️", callback_data=f"remove_page_{page + 1}"))
        if nav_buttons:
            keyboard_buttons.append(nav_buttons)
    
    keyboard = InlineKeyboardMarkup(keyboard_buttons)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            reply_markup=keyboard,
            parse_mode=None  # No markdown to avoid parsing errors
        )
    else:
        await message_obj.reply_text(
            message,
            reply_markup=keyboard,
            parse_mode=None
        )


async def show_links_with_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE, links: List[str], page: int = 0) -> None:
    """Show links with pagination (10 per page) and remove option."""
    LINKS_PER_PAGE = 10
    total_links = len(links)
    total_pages = (total_links + LINKS_PER_PAGE - 1) // LINKS_PER_PAGE
    
    # Get message object
    if update.callback_query:
        message_obj = update.callback_query.message
    else:
        message_obj = update.message
    
    # Calculate pagination
    start_idx = page * LINKS_PER_PAGE
    end_idx = min(start_idx + LINKS_PER_PAGE, total_links)
    page_links = links[start_idx:end_idx]
    
    # Build message - use plain text for links to avoid markdown parsing issues
    message = f"📎 Collected Links ({total_links} total):\n\n"
    for i, link in enumerate(page_links, start=start_idx + 1):
        # Escape URLs to prevent markdown parsing errors
        message += f"{i}. {link}\n"
    
    if total_pages > 1:
        message += f"\nPage {page + 1} of {total_pages}"
    
    message += "\n\nClick Remove to remove links by number (e.g., 1,3,5 or 1-5)"
    
    # Create keyboard
    keyboard_buttons = []
    
    # Pagination buttons
    if total_pages > 1:
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("◀️ Previous", callback_data=f"links_page_{page - 1}"))
        if page < total_pages - 1:
            nav_buttons.append(InlineKeyboardButton("Next ▶️", callback_data=f"links_page_{page + 1}"))
        if nav_buttons:
            keyboard_buttons.append(nav_buttons)
    
    # Action buttons - only remove, no plan trigger
    keyboard_buttons.append([
        InlineKeyboardButton("🗑️ Remove Links", callback_data="remove_links_mode")
    ])
    keyboard_buttons.append([InlineKeyboardButton("🚀 Return to trip view", callback_data="plan_trip")])
    keyboard = InlineKeyboardMarkup(keyboard_buttons)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            reply_markup=keyboard,
            parse_mode=None  # No markdown to avoid parsing errors with URLs
        )
    else:
        await message_obj.reply_text(
            message,
            reply_markup=keyboard,
            parse_mode=None  # No markdown to avoid parsing errors with URLs
        )


async def update_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /update command - update context questions."""
    init_chat_state(context)
    chat_id = update.effective_chat.id
    
    # Load from Supabase if not in chat_data
    trip = context.chat_data.get("trip", {})
    links = context.chat_data.get("links", [])
    
    # Check if we have trip data in memory
    has_data = has_trip_data(trip)
    
    # If no trip data in memory, try loading from Supabase
    if not has_data:
        existing_trip, existing_links = load_user_data(chat_id)
        if existing_trip:
            context.chat_data["trip"] = {
                "start_date": existing_trip.get("start_date"),
                "duration_days": existing_trip.get("duration"),
                "budget": existing_trip.get("budget"),
                "group_size": existing_trip.get("group_size"),
                "city": existing_trip.get("city"),
            }
            trip = context.chat_data["trip"]
        if existing_links:
            context.chat_data["links"] = existing_links
            links = existing_links
    
    # Get message object (could be from callback query or regular message)
    if update.callback_query:
        message_obj = update.callback_query.message
    else:
        message_obj = update.message
    
    # Check again after loading from Supabase
    has_data = has_trip_data(trip)
    
    if not has_data:
        await message_obj.reply_text(
            "You haven't set up your trip details yet. Use /start to begin! 😊",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Show current values with edit buttons
    message = "✏️ **Update Your Trip Details:**\n\n"
    message += build_trip_summary(trip, links)
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📅 Update Date", callback_data="update_start_date")],
        [InlineKeyboardButton("⏱️ Update Duration", callback_data="update_duration")],
        [InlineKeyboardButton("💰 Update Budget", callback_data="update_budget")],
        [InlineKeyboardButton("👥 Update Group Size", callback_data="update_group_size")],
        [InlineKeyboardButton("🌍 Update City", callback_data="update_city")],
        [InlineKeyboardButton("✅ Done", callback_data="update_done")]
    ])
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await message_obj.reply_text(
            message,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    help_text = (
        "🤖 **HeyMax Trip Planner Bot**\n\n"
        "**Commands:**\n"
        "• /start - Begin setting up your trip details\n"
        "• /plan - Start collecting inspiration links\n"
        "• /links - View and manage your collected links\n"
        "• /confirm - Send your trip summary to the chat\n"
        "• /update - Update your trip details\n"
        "• /help - Show this help message\n\n"
        "**How it works:**\n"
        "1. Use /start to answer questions about your trip\n"
        "2. Use /plan and send me links (YouTube, Instagram, TikTok, Airbnb)\n"
        "3. I'll collect links silently in the background\n"
        "4. When ready, confirm and I'll create your personalized trip plan! ✨"
    )
    
    await update.message.reply_text(
        help_text,
        parse_mode=ParseMode.MARKDOWN
    )

# ---------- Callback Query Handlers ----------

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline button callbacks."""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "start_context":
        context.chat_data["idx"] = 0
        await query.edit_message_text(
            START_DATE_QUESTION,
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif data.startswith("links_page_"):
        page = int(data.split("_")[-1])
        links = context.chat_data.get("links", [])
        await show_links_with_buttons(update, context, links, page=page)
    
    elif data.startswith("remove_page_"):
        page = int(data.split("_")[-1])
        links = context.chat_data.get("links", [])
        context.chat_data["remove_page"] = page
        await show_remove_links_prompt(update, context, links, page=page)
    
    elif data == "remove_links_mode":
        links = context.chat_data.get("links", [])
        context.chat_data["state"] = "removing_links"
        context.chat_data["remove_page"] = 0  # Track pagination for remove mode
        await show_remove_links_prompt(update, context, links, page=0)
    
    elif data == "confirm_links":
        # Start planning - process the trip
        await process_trip(update, context)
        
    elif data == "plan_trip":
        # to call on /plan view
        trip = context.chat_data.get("trip", {})
        links = context.chat_data.get("links", [])
        
        await send_trip_summary_message(update.effective_message, context)
        
    
    elif data == "confirm_trip":
        # Update the original message to show confirmation
        trip = context.chat_data.get("trip", {})
        links = context.chat_data.get("links", [])
        summary = build_trip_summary(trip, links)
        
        await query.edit_message_text(
            f"✅ Perfect! Your trip details are saved.\n\n{summary}\n\n"
            "You can send me links from:\n"
            "• YouTube\n"
            "• Instagram\n"
            "• TikTok\n"
            "• Airbnb\n\n"
            "I'll collect them silently in the background.\n\n"
            f"{NEXT_STEPS}",
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif data == "generate_summary_prompt":
        trip = context.chat_data.get("trip", {})
        if not has_trip_data(trip):
            existing_trip, existing_links = load_user_data(query.message.chat.id)
            if existing_trip:
                context.chat_data["trip"] = {
                    "start_date": existing_trip.get("start_date"),
                    "duration_days": existing_trip.get("duration"),
                    "budget": existing_trip.get("budget"),
                    "group_size": existing_trip.get("group_size"),
                    "city": existing_trip.get("city"),
                }
                trip = context.chat_data["trip"]
            if existing_links:
                context.chat_data["links"] = existing_links
        
        if not has_trip_data(trip):
            await query.answer("Set up your trip first with /start", show_alert=True)
            return
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Yes, share it", callback_data="generate_summary_yes"),
                InlineKeyboardButton("❌ Not yet", callback_data="generate_summary_no")
            ]
        ])
        await query.message.reply_text(
            "Share the current trip summary with the chat?",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif data == "generate_summary_yes":
        sent = await send_trip_summary_message(query.message, context)
        if sent:
            await query.edit_message_text("📝 Trip summary sent!", parse_mode=ParseMode.MARKDOWN)
        else:
            await query.edit_message_text(
                "I still need your trip details first. Use /start to begin!",
                parse_mode=ParseMode.MARKDOWN
            )
    
    elif data == "generate_summary_no":
        await query.edit_message_text("No worries, I won't share it yet.", parse_mode=ParseMode.MARKDOWN)
    
    elif data == "start_fresh":
        # Clear all data and start fresh
        context.chat_data["idx"] = 0
        context.chat_data["state"] = "collecting_context"
        context.chat_data["trip"] = {
            "start_date": None,
            "duration_days": None,
            "budget": None,
            "group_size": None,
            "city": None,
        }
        context.chat_data["links"] = []
        context.chat_data["final_payload"] = None
        
        await query.edit_message_text(
            "🆕 Starting fresh! Let's begin with your trip details.",
            parse_mode=None
        )
        await query.message.reply_text(
            START_DATE_QUESTION,
            parse_mode=ParseMode.MARKDOWN
        )
    
    elif data == "view_links":
        links = context.chat_data.get("links", [])
        if links:
            await show_links_with_buttons(update, context, links)
        else:
            await query.answer("No links found.", show_alert=True)
    
    elif data == "update_trip":
        await update_cmd(update, context)
        return
    
    elif data.startswith("update_"):
        field = data.replace("update_", "")
        if field == "done":
            context.chat_data["updating_field"] = None  # Clear update flag
            keyboard_buttons = []
            keyboard_buttons.append([InlineKeyboardButton("🚀 Return to trip view", callback_data="plan_trip")])
            keyboard = InlineKeyboardMarkup(keyboard_buttons)
            
            await query.edit_message_text(
                f"✅ Your trip details are up to date!",
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            # Map to question index
            field_map = {
                "start_date": 0,
                "duration": 1,
                "budget": 2,
                "group_size": 3,
                "city": 4
            }
            if field in field_map:
                context.chat_data["idx"] = field_map[field]
                context.chat_data["state"] = "collecting_context"
                context.chat_data["updating_field"] = field  # Set flag to track we're updating this field
                questions = [
                    START_DATE_QUESTION,
                    DURATION_QUESTION,
                    BUDGET_QUESTION,
                    GROUP_SIZE_QUESTION,
                    DESTINATION_QUESTION
                ]
                await query.edit_message_text(
                    questions[field_map[field]],
                    parse_mode=ParseMode.MARKDOWN
                )


# ---------- Message Handlers ----------

def parse_link_numbers(text: str, total_links: int) -> List[int]:
    """Parse link numbers from text (supports single, comma-separated, ranges)."""
    numbers = set()
    text = text.strip()
    
    # Split by comma
    parts = [p.strip() for p in text.split(",")]
    
    for part in parts:
        if "-" in part:
            # Range like "1-5"
            try:
                start, end = part.split("-", 1)
                start_num = int(start.strip())
                end_num = int(end.strip())
                if start_num > end_num:
                    start_num, end_num = end_num, start_num
                numbers.update(range(start_num, end_num + 1))
            except ValueError:
                continue
        else:
            # Single number
            try:
                num = int(part)
                if 1 <= num <= total_links:
                    numbers.add(num)
            except ValueError:
                continue
    
    return sorted(list(numbers))


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages - context collection, link detection, and link removal."""
    init_chat_state(context)
    msg = update.effective_message
    text = msg.text or ""
    chat_data = context.chat_data
    
    # Handle link removal mode
    if chat_data.get("state") == "removing_links":
        # /cancel is handled by command handler, so we just process the removal here
        
        links = chat_data.get("links", [])
        if not links:
            chat_data["state"] = "idle"
            chat_data.pop("remove_page", None)
            await msg.reply_text("No links to remove.", parse_mode=None)
            return
        
        # Parse link numbers
        link_numbers = parse_link_numbers(text, len(links))
        
        if not link_numbers:
            # Show current page of links again with format examples
            current_page = chat_data.get("remove_page", 0)
            await show_remove_links_prompt(update, context, links, page=current_page)
            await msg.reply_text(
                "❌ Invalid format. Please enter link numbers.\n\n"
                "Examples:\n"
                "• Single: 1\n"
                "• Multiple: 1,3,5\n"
                "• Range: 1-5\n"
                "• Mixed: 1,3-5,7\n\n"
                "Type /cancel to cancel.",
                parse_mode=None
            )
            return
        
        # Remove links (in reverse order to maintain indices)
        removed_links = []
        for num in sorted(link_numbers, reverse=True):
            idx = num - 1  # Convert to 0-based index
            if 0 <= idx < len(links):
                removed_link = links.pop(idx)
                removed_links.append(removed_link)
                remove_link_database(msg.chat.id, removed_link)
        
        if removed_links:
            removed_text = "\n".join(f"  • {link}" for link in removed_links)
            await msg.reply_text(
                f"✅ Removed {len(removed_links)} link(s):\n\n{removed_text}\n\n"
                f"Remaining: {len(links)} link(s)",
                parse_mode=None
            )
            chat_data["state"] = "idle"
            chat_data.pop("remove_page", None)  # Clear remove page state
            
            # Show updated list
            if links:
                await show_links_with_buttons(update, context, links)
            else:
                await msg.reply_text("📭 No links remaining.", parse_mode=None)
        else:
            await msg.reply_text("❌ No valid links found to remove.", parse_mode=None)
        
        return
    
    # Extract URLs from message
    found_links = URL_RE.findall(text)
    
    # Silently collect valid links in background
    if found_links:
        for url in found_links:
            # Clean URL: remove @ prefix and any leading whitespace
            cleaned_url = url.strip().lstrip('@')
            if cleaned_url and is_allowed_platform(cleaned_url):
                links = chat_data.get("links", [])
                if cleaned_url not in links:  # Avoid duplicates
                    links.append(cleaned_url)
                    chat_data["links"] = links
                    add_link(msg.chat.id, [cleaned_url])  # Save to Supabase
    
    # Handle context collection
    if chat_data.get("state") == "collecting_context":
        await handle_context_answer(update, context, text)
        return
    
    # If not in context collection mode and message contains only links, acknowledge silently
    if found_links and all(is_allowed_platform(url) for url in found_links):
        # Links are already collected above, no need to respond
        return


def validate_date(date_str: str) -> Tuple[bool, Optional[str]]:
    """Validate and normalize date input. Returns (is_valid, normalized_date or error_message)."""
    date_str = date_str.strip()
    
    # Try YYYY-MM-DD format
    iso = to_iso(date_str)
    if iso:
        # Check if date is in the future
        try:
            dt = datetime.strptime(iso, "%Y-%m-%d")
            if dt.date() < datetime.now().date():
                return False, "❌ Please enter a future date. Your trip date should be in the future!"
            return True, iso
        except:
            pass
    
    # Try other common formats
    formats = ["%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y", "%m-%d-%Y", "%m/%d/%Y", "%d.%m.%Y", "%Y.%m.%d"]
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            if dt.date() < datetime.now().date():
                return False, "❌ Please enter a future date. Your trip date should be in the future!"
            return True, dt.strftime("%Y-%m-%d")
        except:
            continue
    
    return False, "❌ Invalid date format. Please use YYYY-MM-DD (e.g., 2025-12-25) or DD-MM-YYYY (e.g., 25-12-2025)"


def validate_duration(duration_str: str) -> Tuple[bool, Optional[int], Optional[str]]:
    """Validate duration input. Returns (is_valid, days or None, error_message or None)."""
    duration_str = duration_str.strip()
    
    # Remove common words
    duration_str = re.sub(r'\s*(days?|day|d)\s*', '', duration_str, flags=re.IGNORECASE)
    
    try:
        days = int(duration_str)
        if days <= 0:
            return False, None, "❌ Please enter a positive number of days (e.g., 5)"
        if days > 365:
            return False, None, "❌ That's a very long trip! Please enter a duration up to 365 days."
        return True, days, None
    except ValueError:
        return False, None, "❌ Please enter a number (e.g., 5 for 5 days)"


def validate_budget(budget_str: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """Validate budget input. Returns (is_valid, normalized_budget or None, error_message or None)."""
    budget_str = budget_str.strip()
    
    if not budget_str or len(budget_str) < 2:
        return False, None, "❌ Please enter a valid budget (e.g., 2000 SGD or 'mid-range')"
    
    # Allow any text for budget (flexible)
    if len(budget_str) > 100:
        return False, None, "❌ Budget description is too long. Please keep it under 100 characters."
    
    return True, budget_str, None


def validate_group_size(size_str: str) -> Tuple[bool, Optional[int], Optional[str]]:
    """Validate group size input. Returns (is_valid, size or None, error_message or None)."""
    size_str = size_str.strip()
    
    # Remove common words
    size_str = re.sub(r'\s*(people?|person|pax|guests?)\s*', '', size_str, flags=re.IGNORECASE)
    
    try:
        size = int(size_str)
        if size < 1:
            return False, None, "❌ Please enter a group size of at least 1 person"
        if size > 100:
            return False, None, "❌ That's a very large group! Please enter a group size up to 100 people."
        return True, size, None
    except ValueError:
        return False, None, "❌ Please enter a number (e.g., 4 for 4 people)"


def validate_city(city_str: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """Validate city input. Returns (is_valid, normalized_city or None, error_message or None)."""
    city_str = city_str.strip()
    
    if not city_str or len(city_str) < 2:
        return False, None, "❌ Please enter a valid city name (at least 2 characters)"
    
    if len(city_str) > 100:
        return False, None, "❌ City name is too long. Please keep it under 100 characters."
    
    # Capitalize first letter of each word
    city = ' '.join(word.capitalize() for word in city_str.split())
    
    return True, city, None


async def handle_context_answer(update: Update, context: ContextTypes.DEFAULT_TYPE, answer_text: str) -> None:
    """Handle answers to context questions with improved validation."""
    chat_data = context.chat_data
    idx = chat_data["idx"]
    updating_field = chat_data.get("updating_field")  # Check if we're updating a single field
    
    if idx >= len(QUESTIONS):
        return
    
    q = QUESTIONS[idx]
    trip = chat_data["trip"]
    chat_id = update.effective_chat.id
    
    # Handle start_date
    if q == "start_date":
        is_valid, result = validate_date(answer_text)
        if not is_valid:
            await update.message.reply_text(result, parse_mode=None)
            return
        trip["start_date"] = result
        
        # If updating single field, save only this field and return to update menu
        if updating_field == "start_date":
            update_single_field(chat_id, "start_date", result)
            chat_data["updating_field"] = None
            chat_data["state"] = "idle"
            # Reload from Supabase to ensure we have latest data
            existing_trip, _ = load_user_data(chat_id)
            if existing_trip:
                context.chat_data["trip"]["start_date"] = existing_trip.get("start_date")
            await update.message.reply_text("✅ Start date updated!", parse_mode=None)
            await update_cmd(update, context)  # Return to update menu
            return
        
        chat_data["idx"] += 1
        await update.message.reply_text(DURATION_QUESTION, parse_mode=ParseMode.MARKDOWN)
        return
    
    # Handle duration
    if q == "duration":
        is_valid, days, error = validate_duration(answer_text)
        if not is_valid:
            await update.message.reply_text(error, parse_mode=None)
            return
        trip["duration_days"] = days
        
        # If updating single field, save only this field and return to update menu
        if updating_field == "duration":
            update_single_field(chat_id, "duration_days", days)
            chat_data["updating_field"] = None
            chat_data["state"] = "idle"
            # Reload from Supabase to ensure we have latest data
            existing_trip, _ = load_user_data(chat_id)
            if existing_trip:
                context.chat_data["trip"]["duration_days"] = existing_trip.get("duration")
            await update.message.reply_text("✅ Duration updated!", parse_mode=None)
            await update_cmd(update, context)  # Return to update menu
            return
        
        chat_data["idx"] += 1
        await update.message.reply_text(BUDGET_QUESTION, parse_mode=ParseMode.MARKDOWN)
        return
    
    # Handle budget
    if q == "budget":
        is_valid, budget, error = validate_budget(answer_text)
        if not is_valid:
            await update.message.reply_text(error, parse_mode=None)
            return
        trip["budget"] = budget
        
        # If updating single field, save only this field and return to update menu
        if updating_field == "budget":
            update_single_field(chat_id, "budget", budget)
            chat_data["updating_field"] = None
            chat_data["state"] = "idle"
            # Reload from Supabase to ensure we have latest data
            existing_trip, _ = load_user_data(chat_id)
            if existing_trip:
                context.chat_data["trip"]["budget"] = existing_trip.get("budget")
            await update.message.reply_text("✅ Budget updated!", parse_mode=None)
            await update_cmd(update, context)  # Return to update menu
            return
        
        chat_data["idx"] += 1
        await update.message.reply_text(GROUP_SIZE_QUESTION, parse_mode=ParseMode.MARKDOWN)
        return
    
    # Handle group_size
    if q == "group_size":
        is_valid, size, error = validate_group_size(answer_text)
        if not is_valid:
            await update.message.reply_text(error, parse_mode=None)
            return
        trip["group_size"] = size
        
        # If updating single field, save only this field and return to update menu
        if updating_field == "group_size":
            update_single_field(chat_id, "group_size", size)
            chat_data["updating_field"] = None
            chat_data["state"] = "idle"
            # Reload from Supabase to ensure we have latest data
            existing_trip, _ = load_user_data(chat_id)
            if existing_trip:
                context.chat_data["trip"]["group_size"] = existing_trip.get("group_size")
            await update.message.reply_text("✅ Group size updated!", parse_mode=None)
            await update_cmd(update, context)  # Return to update menu
            return
        
        chat_data["idx"] += 1
        await update.message.reply_text(DESTINATION_QUESTION, parse_mode=ParseMode.MARKDOWN)
        return
    
    # Handle city
    if q == "city":
        is_valid, city, error = validate_city(answer_text)
        if not is_valid:
            await update.message.reply_text(error, parse_mode=None)
            return
        trip["city"] = city
        
        # If updating single field, save only this field and return to update menu
        if updating_field == "city":
            update_single_field(chat_id, "city", city)
            chat_data["updating_field"] = None
            chat_data["state"] = "idle"
            # Reload from Supabase to ensure we have latest data
            existing_trip, _ = load_user_data(chat_id)
            if existing_trip:
                context.chat_data["trip"]["city"] = existing_trip.get("city")
            await update.message.reply_text("✅ City updated!", parse_mode=None)
            await update_cmd(update, context)  # Return to update menu
            return
        
        # Build final payload (only for initial collection, not updates)
        payload = {
            "user_id": str(update.effective_user.id),
            "chat_id": str(update.effective_chat.id),
            "trip": trip,
            "meta": {
                "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
                "version": "v1",
                "mode": "group" if update.effective_chat.type in ("group", "supergroup") else "dm",
            },
        }
        chat_data["final_payload"] = payload
        chat_data["idx"] = len(QUESTIONS)
        chat_data["state"] = "idle"
        
        # Show summary with confirmation
        summary = build_trip_summary(trip, chat_data.get("links", []))
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Start sending links", callback_data="confirm_trip")],
            [InlineKeyboardButton("✏️ Update Details", callback_data="update_trip")]
        ])
        
        await update.message.reply_text(
            f"🎉 Great! Here's what I've got:\n\n{summary}\n\nReady to create your trip plan?",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )


async def process_trip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process trip: extract transcripts, call OpenAI planner, return results."""
    chat_data = context.chat_data
    payload = chat_data.get("final_payload")
    
    # Get message object (could be from callback query or regular message)
    if update.callback_query:
        query = update.callback_query
        message = query.message
        await query.answer()
    else:
        message = update.message
    
    if not payload:
        if update.callback_query:
            await update.callback_query.answer("Please complete your trip details first!", show_alert=True)
        else:
            await message.reply_text("Please complete your trip details first! Use /start to begin.")
        return
    
    # Check if we have links
    raw_links = chat_data.get("links", [])
    if not raw_links or len(raw_links) == 0:
        error_message = (
            "❌ Too little information to plan a trip!\n\n"
            "I need at least some inspiration links to create your personalized trip plan.\n\n"
            "Please collect some links from:\n"
            "• YouTube\n"
            "• Instagram\n"
            "• TikTok\n"
            "• Airbnb\n\n"
            "Use /plan to start collecting links, or just send me links directly! ✨"
        )
        if update.callback_query:
            await update.callback_query.answer("Need links to plan!", show_alert=True)
        await message.reply_text(error_message, parse_mode=None)
        return
    
    # Show processing message
    processing_msg = await message.reply_text(PROCESSING_MESSAGE)
    
    try:
        # Group links by platform
        raw_links = chat_data.get("links", [])
        grouped_links = group_links_by_domain(raw_links)
        
        # Log what platforms we're processing
        print(f"Processing links from platforms: {list(grouped_links.keys())}")
        for platform, urls in grouped_links.items():
            print(f"  {platform}: {len(urls)} link(s)")
        
        # Extract transcripts
        extracted_results = process_links_batch(grouped_links)
        
        # Log extraction results
        print(f"\n{'='*60}")
        print(f"Extraction completed: {len(extracted_results)} results")
        print(f"{'='*60}")
        for result in extracted_results:
            link_data = result.get("link", {})
            platform = link_data.get("platform", "unknown")
            url = link_data.get("url", "")
            transcript = link_data.get("transcript", "")
            status = link_data.get("status", result.get("status", "unknown"))
            error = link_data.get("error", result.get("error"))
            
            print(f"\n{platform.upper()}:")
            print(f"  URL: {url}")
            print(f"  Status: {status}")
            if error:
                print(f"  Error: {error}")
            print(f"  Transcript length: {len(transcript)} characters")
            if transcript:
                print(f"  Preview: {transcript[:100]}...")
        
        # Save extracted results to output.json
        output_data = {
            "trip_context": payload["trip"],
            "extracted_links": extracted_results,
            "extraction_timestamp": datetime.now(timezone.utc).isoformat(),
            "total_links": len(raw_links),
            "platforms_processed": list(grouped_links.keys()),
            "summary": {
                "total_extracted": len(extracted_results),
                "by_platform": {},
                "by_status": {}
            }
        }
        
        # Calculate summary statistics
        for result in extracted_results:
            link_data = result.get("link", {})
            platform = link_data.get("platform", "unknown")
            status = link_data.get("status", "unknown")
            
            # Count by platform
            if platform not in output_data["summary"]["by_platform"]:
                output_data["summary"]["by_platform"][platform] = 0
            output_data["summary"]["by_platform"][platform] += 1
            
            # Count by status
            if status not in output_data["summary"]["by_status"]:
                output_data["summary"]["by_status"][status] = 0
            output_data["summary"]["by_status"][status] += 1
        
        output_file = "output.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"\n{'='*60}")
        print(f"✅ Saved extraction results to {output_file}")
        print(f"   Summary: {output_data['summary']}")
        print(f"{'='*60}\n")
        
        # Format payload for OpenAI planner
        planner_inputs = format_planner_payload(payload["trip"], extracted_results)
        
        # Call OpenAI API
        planner_client = OpenAIPlanner()
        planner_response = planner_client.call_planner(planner_inputs)
        
        # Save planner response to JSON
        planner_output = {
            "trip_context": payload["trip"],
            "planner_response": planner_response,
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
            "extracted_links_count": len(extracted_results),
        }
        planner_json_file = "planner_output.json"
        with open(planner_json_file, "w", encoding="utf-8") as f:
            json.dump(planner_output, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved planner response to {planner_json_file}")
        
        # Generate markdown file from planner response
        markdown_file = "trip_plan.md"
        with open(markdown_file, "w", encoding="utf-8") as f:
            f.write(f"# Trip Plan: {payload['trip'].get('city', 'Unknown')}\n\n")
            f.write(f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")
            f.write("---\n\n")
            f.write(planner_response)
        print(f"✅ Generated markdown file: {markdown_file}")
        
        # Update database
        json_trip_data = json.dumps(payload, indent=2)
        # update_database expects an update object, but we can pass the message's update
        # or create a minimal one if needed
        if update.effective_chat:
            update_database(update, payload, json_trip_data)
        else:
            # Fallback: create minimal update-like object
            class MinimalUpdate:
                def __init__(self, chat_id, user_id):
                    self.effective_chat = type('obj', (object,), {'id': chat_id})()
                    self.effective_user = type('obj', (object,), {'id': user_id})()
            minimal_update = MinimalUpdate(message.chat.id, message.from_user.id if message.from_user else 0)
            update_database(minimal_update, payload, json_trip_data)
        add_link(message.chat.id, raw_links)
        
        # Send formatted response
        await processing_msg.delete()
        await message.reply_text(
            f"✨ **Your Personalized Trip Plan:**\n\n{planner_response}",
            parse_mode=ParseMode.MARKDOWN
        )
        
    except Exception as e:
        await processing_msg.delete()
        await message.reply_text(
            f"❌ Oops! Something went wrong: {str(e)}\n\nPlease try again or contact support.",
            parse_mode=ParseMode.MARKDOWN
        )
        print(f"Error processing trip: {e}")


async def cancel_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /cancel command."""
    chat_data = context.chat_data
    state = chat_data.get("state")
    
    if state == "removing_links":
        chat_data["state"] = "idle"
        chat_data.pop("remove_page", None)
        await update.message.reply_text("❌ Link removal cancelled.", parse_mode=None)
        links = chat_data.get("links", [])
        if links:
            await show_links_with_buttons(update, context, links)
    elif state == "collecting_context":
        chat_data["state"] = "idle"
        chat_data["idx"] = 0
        await update.message.reply_text("❌ Context collection cancelled.", parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text("Nothing to cancel.", parse_mode=ParseMode.MARKDOWN)


async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle when bot is added to a group."""
    if not update.message or not update.message.new_chat_members:
        return
    
    bot_info = await context.bot.get_me()
    bot_username = bot_info.username
    
    # Check if bot was added
    for member in update.message.new_chat_members:
        if member.id == bot_info.id:
            welcome_message = (
                f"👋 Hey everyone! I'm **HeyMax Trip Planner Bot**!\n\n"
                f"I help groups plan amazing trips by collecting trip details and inspiration links.\n\n"
                f"To learn more about what I can do, please run **/help** to see all available commands!\n\n"
                f"Let's plan something awesome together! 🚀"
            )
            await update.message.reply_text(
                welcome_message,
                parse_mode=ParseMode.MARKDOWN
            )
            break


def build_app() -> Application:
    """Build and configure the Telegram bot application."""
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("plan", plan))
    app.add_handler(CommandHandler("links", links_cmd))
    app.add_handler(CommandHandler("update", update_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("cancel", cancel_cmd))
    
    # Group join handler
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))
    
    # Callback query handler (for buttons)
    app.add_handler(CallbackQueryHandler(handle_callback))
    
    # Message handler (for context collection and link detection)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.UpdateType.EDITED, handle_message))
    
    return app


if __name__ == "__main__":
    import logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    
    application = build_app()
    print("🤖 HeyMax Trip Planner Bot is running...")
    application.run_polling(allowed_updates=None)

