from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.main import lifespan


class TestLifespan:
    async def test_lifespan_startup(self):
        """lifespan calls configure_logging, migrations, and seeding in order."""
        mock_app = MagicMock()

        with (
            patch("src.main.configure_logging") as mock_log,
            patch("src.main.run_migrations") as mock_mig,
            patch("src.main.seed_superuser") as mock_seed,
            patch("src.main.engine") as mock_engine,
        ):
            mock_engine.dispose = AsyncMock()

            async with lifespan(mock_app):
                mock_log.assert_called_once()
                mock_mig.assert_called_once()
                mock_seed.assert_called_once()

            mock_engine.dispose.assert_called_once()

    async def test_lifespan_migration_failure(self):
        """If run_migrations fails, it is logged and re-raised."""
        mock_app = MagicMock()

        with (
            patch("src.main.configure_logging"),
            patch("src.main.run_migrations", side_effect=RuntimeError("db down")),
            patch("src.main.seed_superuser") as mock_seed,
            patch("src.main.engine") as mock_engine,
        ):
            mock_engine.dispose = AsyncMock()

            with pytest.raises(RuntimeError, match="db down"):
                async with lifespan(mock_app):
                    pass

            mock_seed.assert_not_called()
