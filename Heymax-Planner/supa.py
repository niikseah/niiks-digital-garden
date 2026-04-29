import os
from dotenv import load_dotenv

# Try to import Supabase - required for operation
try:
    from supabase import create_client, Client, ClientOptions
    SUPABASE_AVAILABLE = True
except ImportError as e:
    SUPABASE_AVAILABLE = False
    error_msg = str(e)
    print(f"❌ ERROR: Supabase import failed: {e}")
    print("   Please install supabase: pip install supabase")
    print("   Or use: pip install --upgrade supabase")
    if "incompatible architecture" in error_msg.lower():
        print("   Architecture mismatch detected. Try:")
        print("   - Install Rosetta 2 (for Intel compatibility)")
        print("   - Or use a virtual environment with correct architecture")
        print("   - Or install via: arch -x86_64 pip install supabase")
    raise RuntimeError("Supabase is required but not available. Please install it.")

# --- Init Supabase client from env ---
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SERVICE_ROLE_KEY:
    raise RuntimeError(
        "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env file. "
        "Supabase is required for the bot to function."
    )

try:
    supabase: Client = create_client(
        SUPABASE_URL,
        SERVICE_ROLE_KEY,
        options=ClientOptions(
            auto_refresh_token=False,
            persist_session=False,
        ),
    )
    print("✅ Supabase client initialized successfully")
except Exception as e:
    print(f"❌ ERROR: Failed to initialize Supabase client: {e}")
    print("   Please check your SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in .env")
    raise RuntimeError(f"Failed to initialize Supabase: {e}")


def update_database(update, payload, json_trip_data):
    """Upsert trip context to user_answers table."""
    
    try:
        response = ( 
            supabase.table("user_answers")
            .upsert({
                "chat_id": update.effective_chat.id,
                "user_id": update.effective_user.id,
                "start_date": payload["trip"]["start_date"],
                "duration": payload["trip"]["duration_days"],
                "budget": payload["trip"]["budget"],
                "city": payload["trip"]["city"],
                "group_size": payload["trip"]["group_size"],
                "json_trip_data": json_trip_data
            }, on_conflict="chat_id")
            .execute()
        )
        if(response):
            print("Supabase upsert response:", response.data)
    except Exception as e:
        print(f"Error updating database: {e}")


def add_link(chat_id: int, links: list[str]):
    """Store collected links to links table."""
    
    try:
        rows = [{"chat_id": chat_id, "link": u} for u in links]
        resp = (
            supabase.table("links")
            # avoid duplicates by PRIMARY KEY (chat_id, link)
            .upsert(rows, on_conflict="chat_id,link")  
            .execute()
        )
        print("Upserted:", resp.data)
    except Exception as e:
        print(f"Error adding links to database: {e}")


def remove_link_database(chat_id: int, link: str):
    """Delete link from links table."""
    
    try:
        resp = (
            supabase.table("links")
            .delete()
            .eq("chat_id", chat_id)
            .eq("link", link)
            .execute()
        )
        print("Removed link:", resp.data)
    except Exception as e:
        print(f"Error removing link from database: {e}")


def update_single_field(chat_id: int, field_name: str, field_value):
    """Update a single field in user_answers table. Only updates that specific field."""
    
    try:
        # Map bot field names to database column names
        field_mapping = {
            "start_date": "start_date",
            "duration": "duration",
            "duration_days": "duration",  # Handle both names
            "budget": "budget",
            "group_size": "group_size",
            "city": "city"
        }
        
        db_field_name = field_mapping.get(field_name, field_name)
        
        # First check if record exists
        existing = (
            supabase.table("user_answers")
            .select("chat_id")
            .eq("chat_id", chat_id)
            .execute()
        )
        
        if existing.data and len(existing.data) > 0:
            # Record exists, update only this field
            response = (
                supabase.table("user_answers")
                .update({db_field_name: field_value})
                .eq("chat_id", chat_id)
                .execute()
            )
            print(f"Updated {db_field_name} for chat_id {chat_id}: {response.data}")
            return True
        else:
            # Record doesn't exist, create it with just this field
            # We need user_id, but we don't have it here. For now, just update with chat_id
            response = (
                supabase.table("user_answers")
                .upsert({
                    "chat_id": chat_id,
                    db_field_name: field_value
                }, on_conflict="chat_id")
                .execute()
            )
            print(f"Created record with {db_field_name} for chat_id {chat_id}: {response.data}")
            return True
    except Exception as e:
        print(f"Error updating single field {field_name}: {e}")
        return False


def load_user_data(chat_id: int):
    """Load existing user trip data and links from Supabase."""
    
    try:
        # Load trip context
        trip_response = (
            supabase.table("user_answers")
            .select("start_date, duration, budget, city, group_size")
            .eq("chat_id", chat_id)
            .execute()
        )
        
        trip_data = None
        if trip_response.data and len(trip_response.data) > 0:
            trip_data = trip_response.data[0]
        
        # Load links
        links_response = (
            supabase.table("links")
            .select("link")
            .eq("chat_id", chat_id)
            .execute()
        )
        
        links = []
        if links_response.data:
            links = [item["link"] for item in links_response.data]
        
        return trip_data, links
    except Exception as e:
        print(f"Error loading user data from database: {e}")
        return None, []

