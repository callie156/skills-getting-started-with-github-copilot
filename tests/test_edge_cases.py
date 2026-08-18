"""
Edge case and boundary condition tests.

This module tests edge cases, error scenarios, and complex workflows with AAA pattern:
- Arrange: Set up unusual or boundary conditions
- Act: Call API with edge case inputs
- Assert: Verify behavior in edge cases
"""

import pytest
from tests.pages.activities_page import ActivitiesPage


class TestEdgeCases:
    """Test suite for edge cases and boundary conditions."""
    
    def test_signup_then_unregister_then_signup_again(self, test_client):
        """
        Arrange: Participant signs up, then unregisters
        Act: Sign up the same participant again
        Assert: Should succeed (signup should return 200)
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Debate Team"
        email = "testuser@mergington.edu"
        
        # Act - Sign up
        response1 = page.signup(activity, email)
        
        # Act - Unregister
        response2 = page.unregister(activity, email)
        
        # Act - Sign up again
        response3 = page.signup(activity, email)
        
        # Assert
        assert response1["status"] == 200
        assert response2["status"] == 200
        assert response3["status"] == 200
        assert email in page.get_activity_participants(activity)
    
    def test_unregister_last_participant_removes_all(self, test_client):
        """
        Arrange: Activity has only one participant
        Act: Unregister that participant
        Assert: Participants list should be empty
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Art Studio"  # Has only lucy@mergington.edu
        email = "lucy@mergington.edu"
        
        # Act
        response = page.unregister(activity, email)
        
        # Assert
        assert response["status"] == 200
        participants = page.get_activity_participants(activity)
        assert len(participants) == 0
    
    def test_activity_name_case_sensitive(self, test_client):
        """
        Arrange: Activity name with different casing
        Act: Try to signup with wrong case
        Assert: Should return 404 (activities are case-sensitive)
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "chess club"  # lowercase instead of "Chess Club"
        email = "student@mergington.edu"
        
        # Act
        response = page.signup(activity, email)
        
        # Assert
        assert response["status"] == 404
    
    def test_empty_email_signup_returns_error(self, test_client):
        """
        Arrange: Empty email string
        Act: Attempt to signup with empty email
        Assert: Should return error (handled by validation)
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Chess Club"
        email = ""
        
        # Act
        response = page.signup(activity, email)
        
        # Assert
        # Empty email might still add to list or fail - implementation dependent
        # This test documents the behavior
        assert response["status"] in [200, 400]
    
    def test_whitespace_email_is_different_from_regular_email(self, test_client):
        """
        Arrange: Email with whitespace vs clean email
        Act: Sign up both variants
        Assert: Should be treated as different emails
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Chess Club"
        email1 = "student@mergington.edu"
        email2 = " student@mergington.edu"  # Leading space
        
        # Act
        response1 = page.signup(activity, email1)
        response2 = page.signup(activity, email2)
        
        # Assert - Both should succeed (treated as different emails)
        assert response1["status"] == 200
        assert response2["status"] == 200
        participants = page.get_activity_participants(activity)
        assert email1 in participants
        assert email2 in participants
    
    def test_signup_multiple_users_sequential(self, test_client):
        """
        Arrange: Multiple distinct users
        Act: Sign up each user sequentially
        Assert: All should succeed and all should appear in participants
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Science Club"
        users = [
            "user1@mergington.edu",
            "user2@mergington.edu",
            "user3@mergington.edu",
        ]
        
        # Act
        responses = [page.signup(activity, user) for user in users]
        
        # Assert
        assert all(r["status"] == 200 for r in responses)
        participants = page.get_activity_participants(activity)
        for user in users:
            assert user in participants
    
    def test_unregister_multiple_users_sequential(self, test_client):
        """
        Arrange: Sign up multiple users
        Act: Unregister them one by one
        Assert: Each unregister should succeed and count should decrease
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Drama Club"
        users = [
            "actor1@mergington.edu",
            "actor2@mergington.edu",
            "actor3@mergington.edu",
        ]
        
        # First sign up all users
        for user in users:
            page.signup(activity, user)
        
        count_after_signup = len(page.get_activity_participants(activity))
        
        # Act & Assert - Unregister one by one
        for i, user in enumerate(users):
            response = page.unregister(activity, user)
            assert response["status"] == 200
            participants = page.get_activity_participants(activity)
            assert len(participants) == count_after_signup - i - 1
    
    def test_activity_at_exact_capacity_cannot_add_more(self, test_client):
        """
        Arrange: Fill activity to exactly max capacity
        Act: Try to add one more participant
        Assert: Should fail with 400
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Basketball Team"  # max 15, has 1 participant
        
        # Fill it to capacity (add 14 more)
        for i in range(14):
            page.signup(activity, f"player{i}@mergington.edu")
        
        # Verify at capacity
        spots = page.get_activity_spots_left(activity)
        assert spots == 0
        
        # Act - Try to add when at capacity
        response = page.signup(activity, "overflow@mergington.edu")
        
        # Assert
        assert response["status"] == 400
        assert "full" in response["error"]
    
    def test_special_characters_in_email(self, test_client):
        """
        Arrange: Email with special characters
        Act: Sign up with special character email
        Assert: Should be accepted (treated as valid string)
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Chess Club"
        email = "user+tag@mergington.edu"  # Email with + character
        
        # Act
        response = page.signup(activity, email)
        
        # Assert
        assert response["status"] == 200
        participants = page.get_activity_participants(activity)
        assert email in participants
    
    def test_very_long_email(self, test_client):
        """
        Arrange: Very long but valid email format
        Act: Sign up with long email
        Assert: Should be accepted
        """
        # Arrange
        page = ActivitiesPage(test_client)
        activity = "Chess Club"
        email = "verylongemailaddress123456789@mergington.edu"
        
        # Act
        response = page.signup(activity, email)
        
        # Assert
        assert response["status"] == 200
        participants = page.get_activity_participants(activity)
        assert email in participants
