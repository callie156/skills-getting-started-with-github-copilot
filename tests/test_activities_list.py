"""
Tests for fetching activities list.

This module tests the GET /activities endpoint with AAA pattern:
- Arrange: Set up test fixtures and initial state
- Act: Call the API endpoint
- Assert: Verify response structure, status, and data integrity
"""

import pytest
from tests.pages.activities_page import ActivitiesPage


class TestActivitiesList:
    """Test suite for GET /activities endpoint."""
    
    def test_get_all_activities_returns_200(self, test_client):
        """
        Arrange: Set up test client with fresh activities
        Act: Fetch all activities
        Assert: Status should be 200 OK
        """
        # Arrange
        page = ActivitiesPage(test_client)
        
        # Act
        response = page.get_activities()
        
        # Assert
        assert response["status"] == 200
    
    def test_get_activities_returns_all_activities(self, test_client):
        """
        Arrange: Set up test client with fresh activities (9 total)
        Act: Fetch all activities
        Assert: Response should contain exactly 9 activities
        """
        # Arrange
        page = ActivitiesPage(test_client)
        expected_count = 9
        
        # Act
        response = page.get_activities()
        activities = response["data"]
        
        # Assert
        assert len(activities) == expected_count
    
    def test_get_activities_has_correct_keys(self, test_client):
        """
        Arrange: Set up test client with fresh activities
        Act: Fetch all activities
        Assert: Each activity should have required fields
        """
        # Arrange
        page = ActivitiesPage(test_client)
        required_keys = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = page.get_activities()
        activities = response["data"]
        
        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert all(key in activity_data for key in required_keys)
    
    def test_get_activities_participants_are_lists(self, test_client):
        """
        Arrange: Set up test client with fresh activities
        Act: Fetch all activities
        Assert: Participants field should always be a list
        """
        # Arrange
        page = ActivitiesPage(test_client)
        
        # Act
        response = page.get_activities()
        activities = response["data"]
        
        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["participants"], list)
            # Each participant should be a string (email)
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)
    
    def test_get_activities_specific_activity_exists(self, test_client):
        """
        Arrange: Set up test client with Chess Club activity
        Act: Fetch all activities
        Assert: Chess Club should exist with correct data
        """
        # Arrange
        page = ActivitiesPage(test_client)
        
        # Act
        response = page.get_activities()
        activities = response["data"]
        
        # Assert
        assert "Chess Club" in activities
        assert activities["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
        assert activities["Chess Club"]["max_participants"] == 12
        assert len(activities["Chess Club"]["participants"]) == 2
    
    def test_no_error_on_successful_get(self, test_client):
        """
        Arrange: Set up test client
        Act: Fetch all activities
        Assert: Error field should be None on success
        """
        # Arrange
        page = ActivitiesPage(test_client)
        
        # Act
        response = page.get_activities()
        
        # Assert
        assert response["error"] is None
