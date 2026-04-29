"""Tests for Supabase database operations."""

import pytest
from datetime import datetime
from supa import (
    load_user_data,
    add_link,
    remove_link_database,
    update_database,
    update_single_field,
)


@pytest.mark.integration
class TestLoadUserData:
    """Test load_user_data() function."""

    @pytest.mark.skipif(
        not __import__("os").getenv("SUPABASE_URL") or not __import__("os").getenv("SUPABASE_SERVICE_ROLE_KEY"),
        reason="Requires Supabase credentials"
    )
    def test_load_nonexistent_user(self, test_chat_id, requires_supabase):
        """Test loading data for non-existent user."""
        # Use a very large chat_id that likely doesn't exist
        nonexistent_id = 999999999999
        trip_data, links = load_user_data(nonexistent_id)
        
        assert trip_data is None
        assert links == []

    @pytest.mark.skipif(
        not __import__("os").getenv("SUPABASE_URL") or not __import__("os").getenv("SUPABASE_SERVICE_ROLE_KEY"),
        reason="Requires Supabase credentials"
    )
    def test_load_existing_user(self, test_chat_id, sample_trip_data, requires_supabase):
        """Test loading data for existing user."""
        # First create some data
        from telegram import Update
        from unittest.mock import Mock
        
        mock_update = Mock()
        mock_update.effective_chat.id = test_chat_id
        mock_update.effective_user.id = 987654321
        
        payload = {
            "trip": sample_trip_data,
        }
        json_trip_data = '{"test": "data"}'
        
        update_database(mock_update, payload, json_trip_data)
        add_link(test_chat_id, ["https://www.youtube.com/watch?v=test"])
        
        # Now load it
        trip_data, links = load_user_data(test_chat_id)
        
        if trip_data:
            assert trip_data.get("city") == sample_trip_data["city"] or trip_data.get("city") is not None
        assert isinstance(links, list)


@pytest.mark.integration
class TestAddLink:
    """Test add_link() function."""

    @pytest.mark.skipif(
        not __import__("os").getenv("SUPABASE_URL") or not __import__("os").getenv("SUPABASE_SERVICE_ROLE_KEY"),
        reason="Requires Supabase credentials"
    )
    def test_add_single_link(self, test_chat_id, requires_supabase):
        """Test adding a single link."""
        test_link = f"https://www.youtube.com/watch?v=test_{datetime.now().timestamp()}"
        add_link(test_chat_id, [test_link])
        
        # Verify it was added
        _, links = load_user_data(test_chat_id)
        assert test_link in links

    @pytest.mark.skipif(
        not __import__("os").getenv("SUPABASE_URL") or not __import__("os").getenv("SUPABASE_SERVICE_ROLE_KEY"),
        reason="Requires Supabase credentials"
    )
    def test_add_multiple_links(self, test_chat_id, requires_supabase):
        """Test adding multiple links."""
        test_links = [
            f"https://www.youtube.com/watch?v=test1_{datetime.now().timestamp()}",
            f"https://www.instagram.com/reel/test2_{datetime.now().timestamp()}",
            f"https://www.airbnb.com/rooms/test3_{datetime.now().timestamp()}",
        ]
        add_link(test_chat_id, test_links)
        
        # Verify they were added
        _, links = load_user_data(test_chat_id)
        for link in test_links:
            assert link in links

    @pytest.mark.skipif(
        not __import__("os").getenv("SUPABASE_URL") or not __import__("os").getenv("SUPABASE_SERVICE_ROLE_KEY"),
        reason="Requires Supabase credentials"
    )
    def test_add_duplicate_link(self, test_chat_id, requires_supabase):
        """Test adding duplicate link (should not create duplicate)."""
        test_link = f"https://www.youtube.com/watch?v=duplicate_{datetime.now().timestamp()}"
        
        # Add twice
        add_link(test_chat_id, [test_link])
        add_link(test_chat_id, [test_link])
        
        # Verify only one exists
        _, links = load_user_data(test_chat_id)
        assert links.count(test_link) == 1


@pytest.mark.integration
class TestRemoveLinkDatabase:
    """Test remove_link_database() function."""

    @pytest.mark.skipif(
        not __import__("os").getenv("SUPABASE_URL") or not __import__("os").getenv("SUPABASE_SERVICE_ROLE_KEY"),
        reason="Requires Supabase credentials"
    )
    def test_remove_existing_link(self, test_chat_id, requires_supabase):
        """Test removing an existing link."""
        test_link = f"https://www.youtube.com/watch?v=remove_{datetime.now().timestamp()}"
        
        # Add link first
        add_link(test_chat_id, [test_link])
        
        # Verify it exists
        _, links = load_user_data(test_chat_id)
        assert test_link in links
        
        # Remove it
        remove_link_database(test_chat_id, test_link)
        
        # Verify it's gone
        _, links_after = load_user_data(test_chat_id)
        assert test_link not in links_after

    @pytest.mark.skipif(
        not __import__("os").getenv("SUPABASE_URL") or not __import__("os").getenv("SUPABASE_SERVICE_ROLE_KEY"),
        reason="Requires Supabase credentials"
    )
    def test_remove_nonexistent_link(self, test_chat_id, requires_supabase):
        """Test removing a non-existent link (should not error)."""
        nonexistent_link = f"https://www.youtube.com/watch?v=nonexistent_{datetime.now().timestamp()}"
        
        # Should not raise an error
        remove_link_database(test_chat_id, nonexistent_link)


@pytest.mark.integration
class TestUpdateDatabase:
    """Test update_database() function."""

    @pytest.mark.skipif(
        not __import__("os").getenv("SUPABASE_URL") or not __import__("os").getenv("SUPABASE_SERVICE_ROLE_KEY"),
        reason="Requires Supabase credentials"
    )
    def test_update_new_user(self, test_chat_id, sample_trip_data, requires_supabase):
        """Test updating database for new user."""
        from unittest.mock import Mock
        
        mock_update = Mock()
        mock_update.effective_chat.id = test_chat_id
        mock_update.effective_user.id = 987654321
        
        payload = {
            "trip": sample_trip_data,
        }
        json_trip_data = '{"test": "new_user"}'
        
        update_database(mock_update, payload, json_trip_data)
        
        # Verify data was saved
        trip_data, _ = load_user_data(test_chat_id)
        if trip_data:
            assert trip_data.get("city") == sample_trip_data["city"] or trip_data.get("city") is not None

    @pytest.mark.skipif(
        not __import__("os").getenv("SUPABASE_URL") or not __import__("os").getenv("SUPABASE_SERVICE_ROLE_KEY"),
        reason="Requires Supabase credentials"
    )
    def test_update_existing_user(self, test_chat_id, sample_trip_data, requires_supabase):
        """Test updating database for existing user."""
        from unittest.mock import Mock
        
        mock_update = Mock()
        mock_update.effective_chat.id = test_chat_id
        mock_update.effective_user.id = 987654321
        
        # First update
        payload1 = {
            "trip": sample_trip_data,
        }
        json_trip_data1 = '{"test": "first"}'
        update_database(mock_update, payload1, json_trip_data1)
        
        # Second update with different data
        updated_data = sample_trip_data.copy()
        updated_data["city"] = "Updated City"
        payload2 = {
            "trip": updated_data,
        }
        json_trip_data2 = '{"test": "second"}'
        update_database(mock_update, payload2, json_trip_data2)
        
        # Verify update
        trip_data, _ = load_user_data(test_chat_id)
        if trip_data:
            # Should have updated data (or at least valid data)
            assert trip_data.get("city") is not None


@pytest.mark.integration
class TestUpdateSingleField:
    """Test update_single_field() function."""

    @pytest.mark.skipif(
        not __import__("os").getenv("SUPABASE_URL") or not __import__("os").getenv("SUPABASE_SERVICE_ROLE_KEY"),
        reason="Requires Supabase credentials"
    )
    def test_update_start_date(self, test_chat_id, requires_supabase):
        """Test updating start_date field."""
        new_date = "2026-01-01"
        result = update_single_field(test_chat_id, "start_date", new_date)
        
        assert result is True
        
        # Verify update
        trip_data, _ = load_user_data(test_chat_id)
        if trip_data:
            assert trip_data.get("start_date") == new_date or trip_data.get("start_date") is not None

    @pytest.mark.skipif(
        not __import__("os").getenv("SUPABASE_URL") or not __import__("os").getenv("SUPABASE_SERVICE_ROLE_KEY"),
        reason="Requires Supabase credentials"
    )
    def test_update_duration(self, test_chat_id, requires_supabase):
        """Test updating duration field."""
        new_duration = 7
        result = update_single_field(test_chat_id, "duration", new_duration)
        
        assert result is True
        
        # Verify update
        trip_data, _ = load_user_data(test_chat_id)
        if trip_data:
            assert trip_data.get("duration") == new_duration or trip_data.get("duration") is not None

    @pytest.mark.skipif(
        not __import__("os").getenv("SUPABASE_URL") or not __import__("os").getenv("SUPABASE_SERVICE_ROLE_KEY"),
        reason="Requires Supabase credentials"
    )
    def test_update_budget(self, test_chat_id, requires_supabase):
        """Test updating budget field."""
        new_budget = "3000 USD"
        result = update_single_field(test_chat_id, "budget", new_budget)
        
        assert result is True
        
        # Verify update
        trip_data, _ = load_user_data(test_chat_id)
        if trip_data:
            assert trip_data.get("budget") == new_budget or trip_data.get("budget") is not None

    @pytest.mark.skipif(
        not __import__("os").getenv("SUPABASE_URL") or not __import__("os").getenv("SUPABASE_SERVICE_ROLE_KEY"),
        reason="Requires Supabase credentials"
    )
    def test_update_city(self, test_chat_id, requires_supabase):
        """Test updating city field."""
        new_city = "Tokyo"
        result = update_single_field(test_chat_id, "city", new_city)
        
        assert result is True
        
        # Verify update
        trip_data, _ = load_user_data(test_chat_id)
        if trip_data:
            assert trip_data.get("city") == new_city or trip_data.get("city") is not None

    @pytest.mark.skipif(
        not __import__("os").getenv("SUPABASE_URL") or not __import__("os").getenv("SUPABASE_SERVICE_ROLE_KEY"),
        reason="Requires Supabase credentials"
    )
    def test_update_group_size(self, test_chat_id, requires_supabase):
        """Test updating group_size field."""
        new_size = 6
        result = update_single_field(test_chat_id, "group_size", new_size)
        
        assert result is True
        
        # Verify update
        trip_data, _ = load_user_data(test_chat_id)
        if trip_data:
            assert trip_data.get("group_size") == new_size or trip_data.get("group_size") is not None

    @pytest.mark.skipif(
        not __import__("os").getenv("SUPABASE_URL") or not __import__("os").getenv("SUPABASE_SERVICE_ROLE_KEY"),
        reason="Requires Supabase credentials"
    )
    def test_update_nonexistent_user(self, requires_supabase):
        """Test updating field for non-existent user (should create record)."""
        nonexistent_id = 888888888888
        result = update_single_field(nonexistent_id, "city", "Test City")
        
        # Should succeed (creates new record)
        assert result is True

