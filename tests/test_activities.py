from src.app import activities

EMAIL = "new.student@mergington.edu"


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert set(data) == set(activities)
    for details in data.values():
        assert {"description", "schedule", "max_participants", "participants"} <= set(details)


def test_signup_adds_participant(client):
    response = client.post("/activities/Art Club/signup", params={"email": EMAIL})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {EMAIL} for Art Club"}
    assert EMAIL in activities["Art Club"]["participants"]


def test_signup_unknown_activity_returns_404(client):
    response = client.post("/activities/Unknown Club/signup", params={"email": EMAIL})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_returns_400(client):
    existing = activities["Chess Club"]["participants"][0]

    response = client.post("/activities/Chess Club/signup", params={"email": existing})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_full_activity_returns_400(client):
    activity = activities["Science Club"]
    activity["participants"] = [f"s{i}@mergington.edu" for i in range(activity["max_participants"])]

    response = client.post("/activities/Science Club/signup", params={"email": EMAIL})

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
    assert EMAIL not in activity["participants"]


def test_unregister_removes_participant(client):
    existing = activities["Gym Class"]["participants"][0]

    response = client.delete("/activities/Gym Class/signup", params={"email": existing})

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {existing} from Gym Class"}
    assert existing not in activities["Gym Class"]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    response = client.delete("/activities/Unknown Club/signup", params={"email": EMAIL})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_non_participant_returns_404(client):
    response = client.delete("/activities/Art Club/signup", params={"email": EMAIL})

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
