"""
Tests for participant signup endpoint.

This module tests the POST /activities/{activity_name}/signup endpoint with AAA pattern:
- Arrange: Set up test fixtures and initial state
- Act: Call the signup API
- Assert: Verify status, error messages, and data updates
"""

import pytest
from tests.pages.activities_page import ActivitiesPage


class TestSignup:
    """Test suite for POST /signup endpoint."""
    
    def test_signup_new_participant_returns_200(self, test_client):
        """
        Arrange: New email not yet registered
        Act: Sign up participant to Chess Club
        Assert: Status should be 200 OK
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Chess Club"
        email = "newemail@mergington.edu"
        
        # Act
        response = page.signup(activity, email)
        
        # Assert
        assert response["status"] == 200
    
    def test_signup_returns_success_message(self, test_client):
        """
        Arrange: New email not yet registered
        Act: Sign up participant
        Assert: Response should contain success message
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Chess Club"
        email = "newemail@mergington.edu"
        
        # Act
        response = page.signup(activity, email)
        
        # Assert
        assert response["message"] is not None
        assert "Signed up" in response["message"]
        assert email in response["message"]
        assert activity in response["message"]
    
    def test_signup_adds_participant_to_activity(self, test_client):
        """
        Arrange: New email not yet registered in Programming Class
        Act: Sign up participant
        Assert: Participant list should be updated
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Programming Class"
        email = "newstudent@mergington.edu"
        
        # Act
        response = page.signup(activity, email)
        
        # Assert
        assert response["status"] == 200
        participants = page.get_activity_participants(activity)
        assert email in participants
    
    def test_signup_duplicate_returns_400(self, test_client):
        """
        Arrange: Already registered participant
        Act: Attempt to sign up same participant again
        Assert: Status should be 400 Bad Request
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club
        
        # Act
        response = page.signup(activity, email)
        
        # Assert
        assert response["status"] == 400
    
    def test_signup_duplicate_error_message(self, test_client):
        """
        Arrange: Already registered participant
        Act: Attempt to sign up same participant again
        Assert: Error message should indicate duplicate
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = page.signup(activity, email)
        
        # Assert
        assert "already signed up" in response["error"]
    
    def test_signup_full_activity_returns_400(self, test_client):
        """
        Arrange: Tennis Club at max capacity (10 participants, 2 slots filled)
        Act: Sign up 9 more participants to fill it
        Act: Try to sign up when full
        Assert: Status should be 400 Bad Request
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Tennis Club"
        
        # Fill up the activity (needs 8 more to reach 10)
        for i in range(8):
            page.signup(activity, f"participant{i}@mergington.edu")
        
        # Act - Try to sign up one more (should fail)
        response = page.signup(activity, "overflow@mergington.edu")
        
        # Assert
        assert response["status"] == 400
    
    def test_signup_full_activity_error_message(self, test_client):
        """
        Arrange: Activity at max capacity
        Act: Attempt to sign up when full
        Assert: Error message should indicate activity is full
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Tennis Club"
        
        # Fill up the activity
        for i in range(8):
            page.signup(activity, f"participant{i}@mergington.edu")
        
        # Act
        response = page.signup(activity, "overflow@mergington.edu")
        
        # Assert
        assert "full" in response["error"]
    
    def test_signup_nonexistent_activity_returns_404(self, test_client):
        """
        Arrange: Nonexistent activity name
        Act: Attempt to sign up for fake activity
        Assert: Status should be 404 Not Found
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Fake Activity"
        email = "student@mergington.edu"
        
        # Act
        response = page.signup(activity, email)
        
        # Assert
        assert response["status"] == 404
    
    def test_signup_nonexistent_activity_error_message(self, test_client):
        """
        Arrange: Nonexistent activity name
        Act: Attempt to sign up
        Assert: Error message should indicate activity not found
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Fake Activity"
        email = "student@mergington.edu"
        
        # Act
        response = page.signup(activity, email)
        
        # Assert
        assert "not found" in response["error"]
    
    def test_signup_updates_available_spots(self, test_client):
        """
        Arrange: Note available spots before signup
        Act: Sign up participant
        Assert: Available spots should decrease by 1
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Art Studio"
        email = "newartist@mergington.edu"
        spots_before = page.get_activity_spots_left(activity)
        
        # Act
        page.signup(activity, email)
        
        # Assert
        spots_after = page.get_activity_spots_left(activity)
        assert spots_after == spots_before - 1
    
    def test_no_error_on_successful_signup(self, test_client):
        """
        Arrange: Valid signup data
        Act: Sign up participant
        Assert: Error field should be None
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Drama Club"
        email = "newactor@mergington.edu"
        
        # Act
        response = page.signup(activity, email)
        
        # Assert
        assert response["error"] is None
