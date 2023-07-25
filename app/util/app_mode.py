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

        match self._app_mode.lower():
            case "prod":
                print("<<<>>> Running in Production Mode")

            case "dev":
                print("<<<>>> Running in Development Mode")

            case "test":
                print("<<<>>> Running in Test Mode")

            case _:
                raise ValueError(
                    f"Invalid APP_MODE environment variable: {self._app_mode}"
                )

    def is_dev(self):
        return self._app_mode == "dev"

    def is_prod(self):
        return self._app_mode == "prod"

    def is_test(self):
        return self._app_mode == "test"

    def get(self):
        return self._app_mode


# Creating App Mode
app_mode = AppMode()

__all__ = ["app_mode"]
