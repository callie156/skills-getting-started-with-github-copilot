"""
Tests for participant unregister endpoint.

This module tests the POST /activities/{activity_name}/unregister endpoint with AAA pattern:
- Arrange: Set up test fixtures and initial state
- Act: Call the unregister API
- Assert: Verify status, error messages, and data updates
"""

import pytest
from tests.pages.activities_page import ActivitiesPage


class TestUnregister:
    """Test suite for POST /unregister endpoint."""
    
    def test_unregister_existing_participant_returns_200(self, test_client):
        """
        Arrange: Participant is registered in Chess Club
        Act: Unregister participant
        Assert: Status should be 200 OK
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club
        
        # Act
        response = page.unregister(activity, email)
        
        # Assert
        assert response["status"] == 200
    
    def test_unregister_returns_success_message(self, test_client):
        """
        Arrange: Participant is registered
        Act: Unregister participant
        Assert: Response should contain success message
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = page.unregister(activity, email)
        
        # Assert
        assert response["message"] is not None
        assert "Unregistered" in response["message"]
        assert email in response["message"]
        assert activity in response["message"]
    
    def test_unregister_removes_participant_from_activity(self, test_client):
        """
        Arrange: Participant is registered
        Act: Unregister participant
        Assert: Participant list should be updated (participant removed)
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = page.unregister(activity, email)
        
        # Assert
        assert response["status"] == 200
        participants = page.get_activity_participants(activity)
        assert email not in participants
    
    def test_unregister_not_registered_returns_400(self, test_client):
        """
        Arrange: Participant not registered in activity
        Act: Attempt to unregister
        Assert: Status should be 400 Bad Request
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Chess Club"
        email = "notregistered@mergington.edu"  # Not in Chess Club
        
        # Act
        response = page.unregister(activity, email)
        
        # Assert
        assert response["status"] == 400
    
    def test_unregister_not_registered_error_message(self, test_client):
        """
        Arrange: Participant not registered
        Act: Attempt to unregister
        Assert: Error message should indicate not registered
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Chess Club"
        email = "notregistered@mergington.edu"
        
        # Act
        response = page.unregister(activity, email)
        
        # Assert
        assert "not registered" in response["error"]
    
    def test_unregister_nonexistent_activity_returns_404(self, test_client):
        """
        Arrange: Nonexistent activity name
        Act: Attempt to unregister from fake activity
        Assert: Status should be 404 Not Found
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Fake Activity"
        email = "student@mergington.edu"
        
        # Act
        response = page.unregister(activity, email)
        
        # Assert
        assert response["status"] == 404
    
    def test_unregister_nonexistent_activity_error_message(self, test_client):
        """
        Arrange: Nonexistent activity name
        Act: Attempt to unregister
        Assert: Error message should indicate activity not found
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Fake Activity"
        email = "student@mergington.edu"
        
        # Act
        response = page.unregister(activity, email)
        
        # Assert
        assert "not found" in response["error"]
    
    def test_unregister_updates_participant_count(self, test_client):
        """
        Arrange: Note participant count before unregister
        Act: Unregister participant
        Assert: Participant count should decrease by 1
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Chess Club"
        email = "michael@mergington.edu"
        count_before = len(page.get_activity_participants(activity))
        
        # Act
        page.unregister(activity, email)
        
        # Assert
        count_after = len(page.get_activity_participants(activity))
        assert count_after == count_before - 1
    
    def test_unregister_updates_available_spots(self, test_client):
        """
        Arrange: Note available spots before unregister
        Act: Unregister participant
        Assert: Available spots should increase by 1
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Chess Club"
        email = "michael@mergington.edu"
        spots_before = page.get_activity_spots_left(activity)
        
        # Act
        page.unregister(activity, email)
        
        # Assert
        spots_after = page.get_activity_spots_left(activity)
        assert spots_after == spots_before + 1
    
    def test_no_error_on_successful_unregister(self, test_client):
        """
        Arrange: Valid unregister data
        Act: Unregister participant
        Assert: Error field should be None
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = page.unregister(activity, email)
        
        # Assert
        assert response["error"] is None
