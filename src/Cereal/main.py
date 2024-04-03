"""Main loop."""

import pandas as pd

from Cereal.API.CerealAPI import CerealAPI
from Cereal.constants import CSV_FILE, DATABASE_URL
from Cereal.server.classes import Cereal
from Cereal.server.connection import SQLConnection


def clean_rating(rating: str) -> float:
    """Clean make ratings into floats.

    Args:
        rating (str): Rating of cereal.

    Returns:
        float: rating as float.
    """
    split = rating.split(".")
    float_rating = float(f"{split[0]}.{split[1]}{split[2]}")
    return float_rating


def main() -> None:
    """Run the main loop."""
    df = pd.read_csv(CSV_FILE, delimiter=";", skiprows=[1])
    df["rating"] = df.rating.apply(clean_rating)
    connection = SQLConnection()

    if connection.is_table_empty(Cereal):
        connection.upload_dataframe(df)

    api = CerealAPI(DATABASE_URL)

    api.run()


if __name__ == "__main__":
    main()
