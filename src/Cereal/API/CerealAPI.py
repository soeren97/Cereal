"""API to connect to the SQL server."""

import logging
from typing import Any, Literal, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Cereal.server.classes import Cereal

logging.basicConfig(level=logging.DEBUG)


class CerealAPI:
    """API class to manipulate data in sql server."""

    def __init__(self, database_url: str):
        """Initialize class.

        Args:
            database_url (str): Url for sql database.
        """
        self.database_url = database_url
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self.app = FastAPI()
        self.setup_routes()

    def setup_routes(self) -> None:
        """Create rutes for API.

        Raises:
            HTTPException: Item not found.
        """

        @self.app.get("/")  # type:ignore
        def main_page() -> dict[str, str]:
            """Execute the main page of API.

            Returns:
                dict[Any]: Welcome message.
            """
            return {"message": "Welcome to my API."}

        @self.app.get("/cereals/{cereal_id}")  # type:ignore
        def read_cereal(cereal_id: int) -> Cereal:
            """Find an item from id.

            Args:
                cereal_id (int): Id of item.

            Raises:
                HTTPException: Item not found.

            Returns:
                Cereal: Item.
            """
            db = self.SessionLocal()
            cereal = db.query(Cereal).filter(Cereal.id == cereal_id).first()
            logging.debug("Cereal found: %s", cereal, "\n")
            db.close()
            if cereal is None:
                raise HTTPException(status_code=404, detail="Cereal not found")
            return cereal

        @self.app.delete("/cereals/{cereal_id}")  # type:ignore
        def delete_cereal(cereal_id: int) -> dict[str, str]:
            """Delete item from id.

            Args:
                cereal_id (int): Id of item.

            Raises:
                HTTPException: Item not found.

            Returns:
                dict[str, str]: Confirmation message.
            """
            logging.debug("Entering delete_cereal route")
            db = self.SessionLocal()
            cereal = db.query(Cereal).filter(Cereal.id == cereal_id).first()
            if cereal is None:
                raise HTTPException(
                    status_code=404, detail=f"Cereal with ID {cereal_id} not found"
                )
            db.delete(cereal)
            db.commit()
            db.close()
            logging.debug("Cereal with ID %s deleted successfully", cereal_id)
            return {"message": f"Cereal with ID {cereal_id} deleted successfully"}

        @self.app.get("/cereals")  # type:ignore
        def search_cereals(
            id: Optional[int] = None,
            name: Optional[str] = None,
            mfr: Optional[str] = None,
            type: Optional[Literal["C", "H"]] = None,
            calories: Optional[int] = None,
            protein: Optional[int] = None,
            fat: Optional[int] = None,
            sodium: Optional[int] = None,
            fiber: Optional[float] = None,
            carbo: Optional[float] = None,
            sugars: Optional[int] = None,
            potass: Optional[int] = None,
            vitamins: Optional[int] = None,
            shelf: Optional[Literal[1, 2, 3]] = None,
            weight: Optional[float] = None,
            cups: Optional[float] = None,
            rating: Optional[float] = None,
        ) -> list[Cereal]:
            """Search by attribute.

            If no inputs are given all items will be returned.

            Args:
                id (Optional[int], optional): Id of cereal. Defaults to None.
                name (Optional[str], optional): Name of cereal. Defaults to None.
                mfr (Optional[str], optional): Manifacturer. Defaults to None.
                type (Optional[Literal["C", "H"]], optional): Is cereal eaten hot or
                    cold. Defaults to None.
                calories (Optional[int], optional): Calories pr serving.
                    Defaults to None.
                protein (Optional[int], optional): proteins pr serving.
                    Defaults to None.
                fat (Optional[int], optional): Fat pr serving. Defaults to None.
                sodium (Optional[int], optional): Sodium pr serving. Defaults to None.
                fiber (Optional[float], optional): Fiber pr serving. Defaults to None.
                carbo (Optional[float], optional): Carbohydrates pr serving.
                    Defaults to None.
                sugars (Optional[int], optional): Sugars pr serving. Defaults to None.
                potass (Optional[int], optional): Potassium pr serving.
                    Defaults to None.
                vitamins (Optional[int], optional): Vitamins pr serving.
                    Defaults to None.
                shelf (Optional[Literal[1, 2, 3]], optional): Display shelf counting
                    from floor. Defaults to None.
                weight (Optional[float], optional): Weight in ounces of one serving.
                    Defaults to None.
                cups (Optional[float], optional): Number of cups in one serving.
                    Defaults to None.
                rating (Optional[float], optional): Rating of the cereals.
                    Defaults to None.

            Raises:
                HTTPException: No items found.

            Returns:
                list[Cereal]: List of results.
            """
            logging.debug("Entering search_cereals route")
            db = self.SessionLocal()
            query = db.query(Cereal)

            filters = {}
            for parameter in [
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
            ]:
                value = locals()[parameter]
                if value is not None:
                    filters[parameter] = value

            cereals = query.filter_by(**filters).all()
            db.close()

            if not cereals:
                raise HTTPException(
                    status_code=404,
                    detail="No cereals found with the specified criteria",
                )

            return cereals  # type: ignore

        @self.app.post("/cereals/")  # type:ignore
        def create_cereal(cereal: Cereal) -> Cereal:
            """Create new entry.

            Args:
                cereal (Cereal): New entry.

            Returns:
                Cereal: New entry.
            """
            db = self.SessionLocal()
            db_cereal = Cereal(**cereal.dict())
            db.add(db_cereal)
            db.commit()
            db.refresh(db_cereal)
            db.close()
            return db_cereal

    def run(self, host: str = "localhost", port: int = 8000) -> None:
        """Run the api.

        Args:
            host (str, optional): Host. Defaults to "localhost".
            port (int, optional): port. Defaults to 8000.
        """
        uvicorn.run(self.app, host=host, port=port)


if __name__ == "__main__":
    pass
