import pytest

from t9_back.lib.serializers.user import User, UserIn


@pytest.fixture()
def user_in(faker):
    return UserIn(email=faker.email(), password=faker.password())


def test_make_password(user_in, faker):
    user = User(email=user_in.email, salt=faker.pystr(), hashed_password=faker.pystr())
    user.make_password(user_in.password)
    assert user.salt is not None
    assert user.hashed_password is not None


@pytest.mark.parametrize(
    "password, salt, hsh_pwd, expected",
    (
        (
            "password",
            "$2b$12$Ai6367CFNgr0uJ5L5HTEmu",
            "$2b$12$imXoZtI7dZGNcYzJ.abaYePoxFkDrkh6aY3i1IEImolIBK0Puxx7y",
            True,
        ),
        ("", "$2b$12$0dVHbE/aMCev/JvhDlRviu", "$2b$12$JibOX55mbrsoQVk2jopzhewiD1Q3ucZY0/yRIz3K6XTessL7fgxXq", True),
        (
            "password1",
            "$2b$12$Ai6367CFNgr0uJ5L5HTEmu",
            "$2b$12$imXoZtI7dZGNcYzJ.abaYePoxFkDrkh6aY3i1IEImolIBK0Puxx7y",
            False,
        ),
    ),
)
def test_check_password(password, salt, hsh_pwd, expected, faker):
    user = User(email=faker.email(), salt=salt, hashed_password=hsh_pwd)
    assert user.check_password(password) == expected
