from src.core.constants import Environment


class TestEnvironment:
    def test_values(self):
        assert Environment.LOCAL == "local"
        assert Environment.STAGING == "staging"
        assert Environment.PRODUCTION == "production"

    def test_is_str_enum(self):
        assert isinstance(Environment.LOCAL, str)
        assert str(Environment.LOCAL) == "local"
