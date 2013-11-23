from tidder.lib.settings import Settings
from tidder.main import main


if __name__ == "__main__":
    settings = Settings()
    main(settings.settings)
