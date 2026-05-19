import pytest
from fastapi.testclient import TestClient


class TestActivities:
    """Tests for the activities endpoints"""

    def test_get_activities_returns_200(self, client):
        """Test that GET /activities returns a 200 status code"""
        # Arrange
        expected_status = 200

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == expected_status

    def test_get_activities_returns_activity_data(self, client):
        """Test that GET /activities returns known activities"""
        # Arrange
        expected_activities = ["Chess Club", "Programming Class", "Gym Class"]

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity in expected_activities:
            assert activity in data
            assert "description" in data[activity]
            assert "schedule" in data[activity]
            assert "max_participants" in data[activity]
            assert "participants" in data[activity]


class TestSignup:
    """Tests for the signup endpoint"""

    def test_signup_for_activity_success(self, client):
        """Test that a new student can successfully sign up for an activity"""
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        expected_status = 200

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == expected_status
        assert "Signed up" in response.json()["message"]

    def test_signup_for_nonexistent_activity_returns_404(self, client):
        """Test that signing up for a non-existent activity returns 404"""
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        expected_status = 404

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == expected_status
        assert "Activity not found" in response.json()["detail"]

    def test_signup_duplicate_email_returns_400(self, client):
        """Test that signing up with a duplicate email returns 400"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already a participant
        expected_status = 400

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == expected_status
        assert "already signed up" in response.json()["detail"]


class TestRemoveParticipant:
    """Tests for the remove participant endpoint"""

    def test_remove_participant_success(self, client):
        """Test that a participant can be successfully removed from an activity"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        expected_status = 200

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == expected_status
        assert "Removed" in response.json()["message"]

    def test_remove_participant_from_nonexistent_activity_returns_404(self, client):
        """Test that removing from non-existent activity returns 404"""
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        expected_status = 404

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == expected_status
        assert "Activity not found" in response.json()["detail"]

    def test_remove_nonexistent_participant_returns_404(self, client):
        """Test that removing a non-existent participant returns 404"""
        # Arrange
        activity_name = "Chess Club"
        email = "nonexistent@mergington.edu"
        expected_status = 404

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )

        # Assert
        assert response.status_code == expected_status
        assert "Participant not found" in response.json()["detail"]
