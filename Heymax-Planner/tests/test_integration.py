"""Full workflow integration tests."""

import pytest
import os
from datetime import datetime
from utils.link_classifier import classify_link, is_allowed_platform
from utils.workflow import process_links_batch
from openai_client import OpenAIPlanner, format_planner_payload
from supa import load_user_data, add_link, update_database, remove_link_database


@pytest.mark.integration
@pytest.mark.api
class TestFullWorkflow:
    """Test complete trip planning workflow."""

    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY"),
        reason="Requires OPENAI_API_KEY for full workflow test"
    )
    def test_complete_happy_path(
        self, test_chat_id, sample_trip_data, requires_openai_key, requires_supabase
    ):
        """Test complete workflow from trip data to plan generation."""
        # Step 1: Create trip data
        from unittest.mock import Mock
        
        mock_update = Mock()
        mock_update.effective_chat.id = test_chat_id
        mock_update.effective_user.id = 987654321
        
        payload = {
            "trip": sample_trip_data,
        }
        json_trip_data = '{"workflow": "test"}'
        
        update_database(mock_update, payload, json_trip_data)
        
        # Verify trip data was saved
        trip_data, _ = load_user_data(test_chat_id)
        assert trip_data is not None
        
        # Step 2: Collect and classify links
        test_links = [
            "https://www.youtube.com/watch?v=jNQXAC9IVRw",  # Real YouTube video
            "https://www.airbnb.com/rooms/12345678",  # Airbnb link
        ]
        
        # Classify links
        classified_links = {}
        for link in test_links:
            platform = classify_link(link)
            assert is_allowed_platform(link), f"Link {link} should be allowed"
            if platform not in classified_links:
                classified_links[platform] = []
            classified_links[platform].append(link)
        
        # Step 3: Save links to database
        add_link(test_chat_id, test_links)
        
        # Verify links were saved
        _, saved_links = load_user_data(test_chat_id)
        for link in test_links:
            assert link in saved_links
        
        # Step 4: Process links through workflow
        extracted_results = process_links_batch(classified_links)
        
        assert len(extracted_results) > 0
        assert all("link" in result for result in extracted_results)
        
        # Step 5: Format payload for OpenAI
        planner_inputs = format_planner_payload(sample_trip_data, extracted_results)
        
        assert "trip_context" in planner_inputs
        assert "extracted_links" in planner_inputs
        assert planner_inputs["trip_context"] == sample_trip_data
        assert len(planner_inputs["extracted_links"]) > 0
        
        # Step 6: Call OpenAI planner
        planner = OpenAIPlanner(mock_mode=False)
        plan_result = planner.call_planner(planner_inputs)
        
        assert isinstance(plan_result, str)
        assert len(plan_result) > 0
        assert "Mock mode" not in plan_result  # Should be real API response
        
        # Cleanup
        for link in test_links:
            remove_link_database(test_chat_id, link)

    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY"),
        reason="Requires OPENAI_API_KEY for full workflow test"
    )
    def test_workflow_with_mixed_success_failure(
        self, test_chat_id, sample_trip_data, requires_openai_key, requires_supabase
    ):
        """Test workflow when some extractors succeed and some fail."""
        # Mix of valid and potentially invalid links
        test_links = {
            "youtube": ["https://www.youtube.com/watch?v=jNQXAC9IVRw"],  # Valid
            "airbnb": ["https://www.airbnb.com/rooms/12345678"],  # Valid (skipped)
            "unknown": ["https://example.com/invalid"],  # Unknown platform
        }
        
        # Process links
        extracted_results = process_links_batch(test_links)
        
        # Should have results even if some fail
        assert len(extracted_results) > 0
        
        # Format and call planner
        planner_inputs = format_planner_payload(sample_trip_data, extracted_results)
        planner = OpenAIPlanner(mock_mode=False)
        
        # Should still work even with mixed results
        plan_result = planner.call_planner(planner_inputs)
        assert isinstance(plan_result, str)
        assert len(plan_result) > 0

    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY"),
        reason="Requires OPENAI_API_KEY for full workflow test"
    )
    def test_workflow_with_empty_links(
        self, sample_trip_data, requires_openai_key
    ):
        """Test workflow with no links (should still generate plan)."""
        empty_links = []
        
        # Format payload
        planner_inputs = format_planner_payload(sample_trip_data, empty_links)
        
        # Call planner
        planner = OpenAIPlanner(mock_mode=False)
        plan_result = planner.call_planner(planner_inputs)
        
        # Should still generate a plan (even without links)
        assert isinstance(plan_result, str)
        assert len(plan_result) > 0

    @pytest.mark.api
    def test_link_collection_and_classification(self, sample_links):
        """Test link collection and classification workflow."""
        all_links = []
        for platform, links in sample_links.items():
            all_links.extend(links)
        
        # Classify all links
        classified = {}
        for link in all_links:
            platform = classify_link(link)
            if platform not in classified:
                classified[platform] = []
            classified[platform].append(link)
        
        # Verify classification
        assert "youtube" in classified or "instagram" in classified or "tiktok" in classified or "airbnb" in classified
        
        # Verify all links are allowed
        for link in all_links:
            if classify_link(link) != "unknown":
                assert is_allowed_platform(link)

    @pytest.mark.api
    def test_data_persistence_workflow(
        self, test_chat_id, sample_trip_data, requires_supabase
    ):
        """Test that data persists correctly through workflow."""
        from unittest.mock import Mock
        
        # Create trip data
        mock_update = Mock()
        mock_update.effective_chat.id = test_chat_id
        mock_update.effective_user.id = 987654321
        
        payload = {
            "trip": sample_trip_data,
        }
        json_trip_data = '{"persistence": "test"}'
        
        update_database(mock_update, payload, json_trip_data)
        
        # Add links
        test_links = [
            f"https://www.youtube.com/watch?v=persist_{datetime.now().timestamp()}",
        ]
        add_link(test_chat_id, test_links)
        
        # Reload data
        trip_data, links = load_user_data(test_chat_id)
        
        # Verify persistence
        assert trip_data is not None
        assert len(links) > 0
        assert test_links[0] in links
        
        # Cleanup
        for link in test_links:
            remove_link_database(test_chat_id, link)

    @pytest.mark.api
    def test_error_recovery_workflow(self, sample_trip_data):
        """Test that workflow handles errors gracefully."""
        # Mix valid and invalid links
        links_map = {
            "youtube": ["https://www.youtube.com/watch?v=jNQXAC9IVRw"],  # Valid
            "youtube": ["https://www.youtube.com/watch?v=INVALID_ID_12345"],  # Invalid
        }
        
        # Process should not crash
        try:
            results = process_links_batch(links_map)
            # Should have at least one result (the valid one)
            assert len(results) >= 1
        except Exception as e:
            pytest.fail(f"Workflow should handle errors gracefully, but raised: {e}")

    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY"),
        reason="Requires OPENAI_API_KEY for full workflow test"
    )
    def test_workflow_with_multiple_platforms(
        self, sample_trip_data, requires_openai_key
    ):
        """Test workflow processing links from multiple platforms."""
        links_map = {
            "youtube": ["https://www.youtube.com/watch?v=jNQXAC9IVRw"],
            "airbnb": [
                "https://www.airbnb.com/rooms/12345678",
                "https://www.airbnb.com/s/singapore",
            ],
        }
        
        # Process links
        extracted_results = process_links_batch(links_map)
        
        # Should have results from all platforms
        platforms = [r["link"]["platform"] for r in extracted_results]
        assert "youtube" in platforms
        assert "airbnb" in platforms
        
        # Format and call planner
        planner_inputs = format_planner_payload(sample_trip_data, extracted_results)
        planner = OpenAIPlanner(mock_mode=False)
        plan_result = planner.call_planner(planner_inputs)
        
        assert isinstance(plan_result, str)
        assert len(plan_result) > 0

