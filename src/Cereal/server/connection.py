"""SQL connection functions."""

from typing import Any, Generator, Union

import pandas as pd
from mysql import connector
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from Cereal.constants import DATABASE_URL, PASSWORD, USERNAME, Base
from Cereal.server.classes import Cereal


class SQLConnection:
    """Class to handle sql connection and queries."""

    _instance = None

    def __new__(cls: Any, *args: tuple[Any], **kwargs: tuple[Any]) -> Any:
        """Make sure there is only one instance of this class.

        Args:
            cls (DatabaseConnection): The class of the instance being created.

        Returns:
            DatabaseConnection: The instance of the DatabaseConnection class.
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize class.

        Args:
            username (str): Username for sql server.
            password (str): Password for sql server.
        """
        self.username = USERNAME
        self.password = PASSWORD
        self.session = self.create_database()

    def create_database(self) -> Session:
        """Create the sql database if not present and connect.

        Returns:
            Session: Connection to sql server.
        """
        connection_mysql = connector.connect(
            host="localhost",
            user=self.username,
            password=self.password,
        )
        cursor = connection_mysql.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS Warehouse")

        # Close the connection
        connection_mysql.close()

        # Now connect to the database
        engine = create_engine(
            DATABASE_URL,
            echo=False,
        )

        Base.metadata.create_all(engine)

        # Create a sessionmaker bound to the engine
        session_maker = sessionmaker(bind=engine)

        # Create a session
        session = session_maker()

        return session

    def upload_dataframe(self, df: pd.DataFrame) -> None:
        """Upload dataframe to sql server.

        Args:
            df (pd.DataFrame): Dataframe to be uploaded.
        """
        # Convert DataFrame to list of dictionaries
        cereals_data = df.to_dict(orient="records")

        # Add the entire list of dictionaries to the session
        self.session.bulk_insert_mappings(Cereal, cereals_data)

        self.session.commit()
        self.session.close()

    def is_table_empty(self, table: type[Cereal]) -> bool:
        """Check if a table is empty.

        Args:
            table (Item): Table to be checked.

        Returns:
            bool: Is table empty.
        """
        # Count the number of rows in the table
        count = self.session.query(table).count()

        # If the count is zero, the table is empty
        return bool(count == 0)
