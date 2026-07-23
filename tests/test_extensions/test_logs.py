import logging

from src.core.config import settings
from src.extensions.logs import configure_logging, get_logger


class TestConfigureLogging:
    def test_configure_logging(self, tmp_path, monkeypatch):
        """configure_logging sets up structlog + root handlers without errors."""
        # Save original state
        root = logging.getLogger()
        original_handlers = root.handlers[:]
        original_level = root.level

        try:
            # Redirect log output to a temp directory
            monkeypatch.setattr(settings, "LOG_DIR", str(tmp_path))

            configure_logging()

            # Root logger should have 2 handlers: console + file
            assert len(root.handlers) == 2
            handler_types = {type(h).__name__ for h in root.handlers}
            assert "StreamHandler" in handler_types
            assert "TimedRotatingFileHandler" in handler_types

            # Log directory should be created
            assert tmp_path.exists()
            log_file = tmp_path / "app.log"
            assert log_file.exists()

            # get_logger returns a working logger
            logger = get_logger("test")
            # May be a BoundLoggerLazyProxy (structlog ≥ 24.x)
            logger.info("test_message", extra="value")
        finally:
            # Restore original state
            root.handlers.clear()
            for h in original_handlers:
                root.addHandler(h)
            root.setLevel(original_level)

    def test_get_logger_returns_usable_logger(self):
        logger = get_logger("my_module")
        # Should be usable regardless of lazy proxy wrapping
        logger.info("test")
