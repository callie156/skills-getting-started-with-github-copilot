"""
Pytest configuration and shared fixtures for API tests.

This module provides:
- App fixture: FastAPI application instance
- Test client fixture: TestClient for making requests
- Activities fixture: Fresh activities data for each test
"""

import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def fresh_activities():
    """
    Provide fresh activities data for each test.
    Uses deep copy to ensure data isolation between tests.
    """
    activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team for intramural and inter-school competitions",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis skills and compete in matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 10,
            "participants": ["james@mergington.edu", "sarah@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and mixed media techniques",
            "schedule": "Mondays and Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["lucy@mergington.edu"]
        },
        "Drama Club": {
            "description": "Act, direct, and perform in theatrical productions",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["noah@mergington.edu", "grace@mergington.edu", "jacob@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop argumentation and public speaking skills through competitive debate",
            "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
            "max_participants": 14,
            "participants": ["maya@mergington.edu"]
        },
        "Science Club": {
            "description": "Explore scientific experiments and STEM projects",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["ryan@mergington.edu", "nina@mergington.edu"]
        }
    }
    return activities


@pytest.fixture
def test_client(fresh_activities, monkeypatch):
    """
    Provide a TestClient with fresh activities data for each test.
    
    Uses monkeypatch to replace the app's activities dict with fresh data,
    ensuring each test starts with clean state and no side effects.
    """
    # Replace the app's activities with fresh data
    monkeypatch.setattr("src.app.activities", fresh_activities)
    
    # Return a test client
    return TestClient(app)
