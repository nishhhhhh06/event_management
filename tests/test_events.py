def test_create_event(client, init_database):
    """Test event creation."""
    client.post("/login", data={"email": "test@example.com", "password": "password123"})
    response = client.post("/events/create", data={
        "title": "New Event",
        "location": "New York",
        "date": "2025-06-10",
        "max_attendees": 100
    }, follow_redirects=True)
    assert b"New Event" in response.data  # Check if event is listed

def test_update_event(client, init_database):
    """Test event update."""
    client.post("/login", data={"email": "test@example.com", "password": "password123"})
    event = init_database[1]
    response = client.post(f"/events/{event.id}/update", data={
        "title": "Updated Event",
        "location": "Updated City",
        "date": "2025-07-10",
        "max_attendees": 150
    }, follow_redirects=True)
    assert b"Updated Event" in response.data

def test_delete_event(client, init_database):
    """Test event deletion."""
    client.post("/login", data={"email": "test@example.com", "password": "password123"})
    event = init_database[1]
    response = client.post(f"/events/{event.id}/delete", follow_redirects=True)
    assert b"Event deleted" in response.data
