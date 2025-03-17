def test_create_user(client, init_database):
    """Test admin creating a user."""
    client.post("/login", data={"email": "test@example.com", "password": "password123"})
    response = client.post("/users/create", data={
        "username": "testuser2",
        "email": "testuser2@example.com",
        "role": "attendee",
        "password": "password123"
    }, follow_redirects=True)
    assert b"User created successfully" in response.data

def test_update_user_role(client, init_database):
    """Test updating user role."""
    client.post("/login", data={"email": "test@example.com", "password": "password123"})
    user = init_database[0]
    response = client.post(f"/users/{user.id}/update", data={"role": "organizer"}, follow_redirects=True)
    assert b"User role updated" in response.data

def test_delete_user(client, init_database):
    """Test deleting a user."""
    client.post("/login", data={"email": "test@example.com", "password": "password123"})
    user = init_database[0]
    response = client.post(f"/users/{user.id}/delete", follow_redirects=True)
    assert b"User deleted successfully" in response.data
