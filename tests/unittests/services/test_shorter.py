import pytest

from t9_back.lib.services.shorter import ShorterService


@pytest.fixture()
def service():
    return ShorterService()


@pytest.mark.parametrize(
    "input, expected",
    (
        (-1, ""),
        (0, "0"),
        (1, "1"),
        (200, "3E"),
        (987654321, "14q60P"),
    ),
)
def test_encode(service: ShorterService, input: int, expected: str):
    assert service.encode(input) == expected


@pytest.mark.parametrize(
    "input, expected",
    (
        ("", 0),
        ("0", 0),
        ("superlongstring", 681063813868063101472163008),
        ("14q60P", 987654321),
    ),
)
def test_decode(service: ShorterService, input: str, expected: int):
    assert service.decode(input) == expected
