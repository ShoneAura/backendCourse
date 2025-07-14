async def test_add_booking(db, ac):
    email = "user@test.com"
    response = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": "123456789",
        },
    )

    assert response.status_code == 200
    res = response.json()
    assert res["status"] == "OK"

    response = await ac.post(
        "/auth/login",
        json={
            "email": "user@test.com",
            "password": "123456789",
        },
    )
    assert response.status_code == 200
    assert ac.cookies["access_token"]

    token = ac.cookies["access_token"]
    print(token)
    headers = {"Authorization": f"Bearer {token}"}
    response_my_bookings = await ac.get("/bookings/me", headers=headers)
    assert response_my_bookings.status_code == 200

    resp_logout = await ac.post("/auth/logout")
    assert resp_logout.status_code == 200
    assert "access_token" not in ac.cookies


#
