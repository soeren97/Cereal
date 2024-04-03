"""Constants used throughout the repocetory."""

import os

from sqlalchemy.ext.declarative import declarative_base

from Cereal.utils import ConfigManager

DATA_FOLDER = "data"

CSV_FILE = os.path.join(DATA_FOLDER, "Cereal.csv")

config_manager = ConfigManager("config.json")

USERNAME = config_manager.username()
PASSWORD = config_manager.password()

DATABASE_URL = f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}" "@localhost/cereal"

Base = declarative_base()

if __name__ == "__name__":
    pass
