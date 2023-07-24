import os


class AppMode:
    _instance = None
    _app_mode = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            cls._instance._configure_appmode()
        return cls._instance

    def _configure_appmode(self):
        self._app_mode = os.getenv("APP_MODE")
        if not self._app_mode:
            raise ValueError("APP_MODE environment variable not set")

        self._app_mode = self._app_mode.lower()
        if self._app_mode == "prod":
            print("Running in Production Mode")
        elif self._app_mode == "dev":
            print("Running in Development Mode")
        elif self._app_mode == "test":
            print("Running in Test Mode")
        else:
            raise ValueError(f"Invalid APP_MODE environment variable: {self._app_mode}")

    def is_dev(self):
        return self._app_mode == "dev"

    def is_prod(self):
        return self._app_mode == "prod"

    def is_test(self):
        return self._app_mode == "test"


# Creating App Mode
app_mode = AppMode()

__all__ = ["app_mode"]
