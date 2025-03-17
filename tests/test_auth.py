def test_register(client):
    """Test user registration."""
    response = client.post("/register", data={
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpassword",
        "confirm_password": "newpassword",
        "role": "attendee"
    }, follow_redirects=True)
    assert b"Account created successfully!" in response.data

def test_login(client, init_database):
    """Test user login."""
    response = client.post("/login", data={
        "email": "test@example.com",
        "password": "password123"
    }, follow_redirects=True)
    assert b"Dashboard" in response.data  # Redirects to dashboard on success

def test_logout(client, init_database):
    """Test user logout."""
    client.post("/login", data={"email": "test@example.com", "password": "password123"})
    response = client.get("/logout", follow_redirects=True)
    assert b"Login" in response.data  # Redirects to login page
