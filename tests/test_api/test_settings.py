import pytest

from volur.api import VolurApiSettings


@pytest.fixture
def expected_settings() -> VolurApiSettings:
    return VolurApiSettings(
        address="fake-address",
        token="fake-token",
    )


def test_settings_should_obtain_configuration_from_environment(
    monkeypatch: pytest.MonkeyPatch,
    expected_settings: VolurApiSettings,
) -> None:
    with monkeypatch.context() as context:
        context.setenv("VOLUR_API_ADDRESS", "fake-address")
        context.setenv("VOLUR_API_TOKEN", "fake-token")
        settings = VolurApiSettings()
    assert expected_settings == settings
