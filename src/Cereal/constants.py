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

VALID_FIELDS = [
    "id",
    "name",
    "mfr",
    "type",
    "calories",
    "protein",
    "fat",
    "sodium",
    "fiber",
    "carbo",
    "sugars",
    "potass",
    "vitamins",
    "shelf",
    "weight",
    "cups",
    "rating",
]

OPERATOR_MAPPING = {
    "eq": lambda field, value: field == value,
    "gt": lambda field, value: field > value,
    "lt": lambda field, value: field < value,
}

if __name__ == "__name__":
    pass
