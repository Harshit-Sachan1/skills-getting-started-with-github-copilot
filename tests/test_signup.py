from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_student_cannot_sign_up_twice_for_same_activity():
    activity_name = "Chess Club"
    email = "duplicate-test@mergington.edu"

    activities[activity_name]["participants"] = []

    first_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert first_response.status_code == 200

    second_response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert second_response.status_code == 400
    assert second_response.json() == {"detail": "Student is already signed up"}


def test_student_can_unregister_from_activity():
    activity_name = "Chess Club"
    email = "remove-test@mergington.edu"

    activities[activity_name]["participants"] = [email]

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
