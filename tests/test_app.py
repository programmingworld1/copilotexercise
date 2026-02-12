import pytest
from fastapi.testclient import TestClient
from src.app import app

# Use a base URL for API endpoints
BASE_URL = "/activities"

client = TestClient(app)

def test_get_activities():
    """Test fetching all activities"""
    response = client.get(BASE_URL)
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data

def test_signup_for_activity_success():
    """Test successful signup for an activity"""
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    signup_url = f"{BASE_URL}/{activity}/signup?email={email}"
    response = client.post(signup_url)
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]

def test_signup_for_activity_duplicate():
    """Test duplicate signup returns error"""
    activity = "Programming Class"
    email = "duplicate@mergington.edu"
    signup_url = f"{BASE_URL}/{activity}/signup?email={email}"
    # Sign up once
    client.post(signup_url)
    # Sign up again
    response = client.post(signup_url)
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"

def test_signup_for_activity_not_found():
    """Test signup for a nonexistent activity returns 404"""
    activity = "Nonexistent"
    email = "ghost@mergington.edu"
    signup_url = f"{BASE_URL}/{activity}/signup?email={email}"
    response = client.post(signup_url)
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
