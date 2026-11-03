import os

from app.core.config import Settings
from app.health import nginx_logs


def _settings() -> Settings:
    os.environ.setdefault("COGNITO_CLIENT_ID", "testing")
    os.environ.setdefault("COGNITO_CLIENT_SECRET", "testing")
    os.environ.setdefault("COGNITO_REGION", "us-east-1")
    os.environ.setdefault("COGNITO_REDIRECT_URI", "testing")
    os.environ.setdefault("COGNITO_USER_POOL_ID", "testing")
    os.environ.setdefault("COGNITO_ACCESS_ID", "testing")
    os.environ.setdefault("COGNITO_ACCESS_KEY", "testing")
    os.environ.setdefault("ROOT_URL", "testing")
    os.environ.setdefault("DATABASE_URL", "testing")
    os.environ.setdefault("LOG_LEVEL", "debug")
    os.environ["HUU_ENVIRONMENT"] = "staging"
    return Settings()


class _FakeFile:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return "log contents"


def test_nginx_logs_reads_both_logs_from_environment_dir(monkeypatch):
    """The error log must be read from the same environment dir as the access log."""
    settings = _settings()
    expected_dir = "/var/log/staging.homeunite.us"

    opened_paths = []

    def fake_open(path, *args, **kwargs):
        opened_paths.append(path)
        return _FakeFile()

    monkeypatch.setattr("builtins.open", fake_open)

    response = nginx_logs(settings)

    assert f"{expected_dir}/nginx-access.log" in opened_paths
    assert f"{expected_dir}/nginx-error.log" in opened_paths
    assert "{nginx_logs_dir}/nginx-error.log" not in opened_paths
    assert response.body == b'{"accessLogs":"log contents","errorLogs":"log contents"}'
