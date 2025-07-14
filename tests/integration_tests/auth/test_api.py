import pytest


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("k0t@pes.com", "1234", 200),
        ("k0t@pes.com", "1234", 400),
        ("k0t1@pes.com", "1235", 200),
        ("abcde", "1235", 422),
        ("abcde@abc", "1235", 422),
    ],
)
async def test_auth_flow(email: str, password: str, status_code: int, ac):
    response_register = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response_register.status_code == status_code
    response_register.json()
    if status_code != 200:
        return

    response_login = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response_login.status_code == status_code
    assert ac.cookies["access_token"]

    response_me = await ac.get("/auth/me")
    assert response_me.status_code == status_code
    response_me_data = response_me.json()
    assert response_me_data["email"] == email
    assert "password" not in response_me_data
    assert "hashed_password" not in response_me_data

    response_logout = await ac.post("/auth/logout")
    assert response_logout.status_code == status_code
    assert "access_token" not in ac.cookies


#
