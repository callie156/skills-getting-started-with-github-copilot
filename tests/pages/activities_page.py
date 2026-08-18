"""
Page Object Model for Activities API.

This module encapsulates all API interactions with the activities endpoints.
Methods return normalized response data for cleaner test code.
"""

from fastapi.testclient import TestClient
from typing import Dict, Any, Optional


class ActivitiesPage:
    """Page object for activities-related API endpoints."""
    
    def __init__(self, client: TestClient):
        """Initialize with a TestClient instance."""
        self.client = client
    
    def get_activities(self) -> Dict[str, Any]:
        """
        Fetch all activities.
        
        Returns:
            Normalized response with status, data, and error info.
        """
        response = self.client.get("/activities")
        
        return {
            "status": response.status_code,
            "data": response.json() if response.status_code == 200 else None,
            "error": None if response.status_code == 200 else response.json().get("detail")
        }
    
    def signup(self, activity_name: str, email: str) -> Dict[str, Any]:
        """
        Sign up a participant for an activity.
        
        Args:
            activity_name: Name of the activity to sign up for.
            email: Email of the participant.
        
        Returns:
            Normalized response with status, message, and error info.
        """
        response = self.client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        result = response.json()
        
        return {
            "status": response.status_code,
            "message": result.get("message"),
            "error": result.get("detail")
        }
    
    def unregister(self, activity_name: str, email: str) -> Dict[str, Any]:
        """
        Unregister a participant from an activity.
        
        Args:
            activity_name: Name of the activity to unregister from.
            email: Email of the participant.
        
        Returns:
            Normalized response with status, message, and error info.
        """
        response = self.client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        result = response.json()
        
        return {
            "status": response.status_code,
            "message": result.get("message"),
            "error": result.get("detail")
        }
    
    def get_activity_participants(self, activity_name: str) -> list:
        """
        Get participants list for a specific activity.
        
        Helper method for assertions.
        
        Args:
            activity_name: Name of the activity.
        
        Returns:
            List of participant emails for the activity, or empty list if not found.
        """
        response = self.get_activities()
        
        if response["status"] != 200:
            return []
        
        activities = response["data"]
        activity = activities.get(activity_name, {})
        
        return activity.get("participants", [])
    
    def get_activity_spots_left(self, activity_name: str) -> Optional[int]:
        """
        Get available spots for a specific activity.
        
        Helper method for assertions.
        
        Args:
            activity_name: Name of the activity.
        
        Returns:
            Number of spots left, or None if activity not found.
        """
        response = self.get_activities()
        
        if response["status"] != 200:
            return None
        
        activities = response["data"]
        activity = activities.get(activity_name, {})
        
        if not activity:
            return None
        
        max_participants = activity.get("max_participants", 0)
        current_participants = len(activity.get("participants", []))
        
        return max_participants - current_participants
