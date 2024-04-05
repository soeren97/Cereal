"""API to connect to the SQL server."""

import logging
from typing import Any, Literal

import uvicorn
from fastapi import FastAPI, HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Cereal.API.classes import APICereal
from Cereal.constants import pwd_context
from Cereal.server.Cereal import Cereal
from Cereal.server.Users import User

logging.basicConfig(level=logging.DEBUG)


FILTER_MAPPING = {
    "id": Cereal.id,
    "name": Cereal.name,
    "mfr": Cereal.mfr,
    "type": Cereal.type,
    "calories": Cereal.calories,
    "protein": Cereal.protein,
    "fat": Cereal.fat,
    "sodium": Cereal.sodium,
    "fiber": Cereal.fiber,
    "carbo": Cereal.carbo,
    "sugars": Cereal.sugars,
    "potass": Cereal.potass,
    "vitamins": Cereal.vitamins,
    "shelf": Cereal.shelf,
    "weight": Cereal.weight,
    "cups": Cereal.cups,
    "rating": Cereal.rating,
}


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

        self.rights = "User"

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

        @self.app.post("/register")  # type:ignore
        def register(username: str, email: str, password: str) -> dict[str, str]:
            """Create new user.

            Args:
                username (str): Username.
                email (str): Email.
                password (str): Password.

            Raises:
                HTTPException: User already exists.

            Returns:
                dict[str, str]: Success message.
            """
            db = self.SessionLocal()
            # Check if user already exists
            if any(user.email == email for user in db):
                raise HTTPException(status_code=400, detail="Email already registered")

            User.create_user(db, username, email, password)

            return {"message": "User registered successfully"}

        @self.app.post("/login")  # type:ignore
        def login(email: str, password: str) -> dict[str, str]:
            """Login as user.

            Args:
                email (str): Email.
                password (str): Password.

            Raises:
                HTTPException: User does not exist.
                HTTPException: Password is incorrect.

            Returns:
                dict[str, str]: Succes message.
            """
            db = self.SessionLocal()
            user = db.query(User).filter(User.email == email).first()
            if not user:
                raise HTTPException(
                    status_code=401,
                    detail="User does not exist.",
                )
            elif not pwd_context.verify(password, user.hashed_password):
                raise HTTPException(
                    status_code=401,
                    detail="Wrong password.",
                )

            db.close()
            self.rights = user.rights
            return {"message": "Login successful"}

        @self.app.get("/cereals/{cereal_id}")  # type:ignore
        def read_cereal(cereal_id: int) -> APICereal:
            """Find an item from id.

            Args:
                cereal_id (int): Id of item.

            Raises:
                HTTPException: Item not found.

            Returns:
                Cereal: Item.
            """
            db = self.SessionLocal()
            cereal = Cereal.get_cereal_by_id(db, cereal_id)
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
            if self.rights != "Admin":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=(
                        "Access denied. "
                        "You are not authorized to access this resource."
                    ),
                )

            db = self.SessionLocal()
            cereal = db.query(Cereal).filter(Cereal.id == cereal_id).first()
            if cereal is None:
                raise HTTPException(
                    status_code=404, detail=f"Cereal with ID {cereal_id} not found"
                )
            db.delete(cereal)
            db.commit()
            db.close()
            return {"message": f"Cereal with ID {cereal_id} deleted successfully"}

        @self.app.get("/cereals")  # type:ignore
        async def search_cereals(
            field: str,
            value: Any,
            operator: Literal["eq", "lt", "gt"],
        ) -> list[APICereal]:
            """Search for cereals with optional filters.

            Args:
                db (Session): Database
                field (Optional[str]): Search filed.
                value (Optional[Any]): Value.
                operator (Optional[Literal["eq", "lt", "gt]]) Operator.

            Returns:
                list[Cereal]: List of found cereal.
            """
            db = self.SessionLocal()

            results = Cereal.get_cereals(db, field, value, operator)

            return results  # type:ignore

        @self.app.post("/cereals/")  # type:ignore
        def create_cereal(cereal: APICereal) -> APICereal:
            """Create or update an entry.

            Args:
                cereal (Cereal): New entry or updated entry.

            Returns:
                APICereal: Created or updated entry.
            """
            db = self.SessionLocal()
            if cereal.id is not None:
                existing_cereal = (
                    db.query(Cereal).filter(Cereal.id == cereal.id).first()
                )
                if existing_cereal:
                    # Update existing entry
                    for key, value in cereal.model_dump().items():
                        setattr(existing_cereal, key, value)
                    db.commit()
                    db.refresh(existing_cereal)
                    db.close()
                    return existing_cereal
                else:
                    raise HTTPException(
                        status_code=404,
                        detail=(
                            "Cereal not found with provided ID "
                            "if you wish to create a new entry "
                            "Make id none."
                        ),
                    )
            else:
                # Create new entry
                if cereal.type in ["C", "H"]:
                    db_cereal = Cereal(**cereal.model_dump())
                    db.add(db_cereal)
                    db.commit()
                    db.refresh(db_cereal)
                    db.close()
                else:
                    raise HTTPException(
                        status_code=422,
                        detail="Invalid value for 'type'. Must be 'C' or 'H'.",
                    )
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
