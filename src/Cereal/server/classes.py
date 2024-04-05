"""SQL schema."""

from typing import Any, Literal, Optional, Type

from fastapi import HTTPException
from sqlalchemy import Column, Enum, Float, Integer, String
from sqlalchemy.orm import Session

from Cereal.constants import VALID_FIELDS, Base


class Cereal(Base):
    """Cereal entity in Cereal database."""

    __tablename__ = "cereal"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    mfr = Column(String(255))
    type = Column(Enum("C", "H", name="type"))
    calories = Column(Integer)
    protein = Column(Integer)
    fat = Column(Integer)
    sodium = Column(Integer)
    fiber = Column(Float)
    carbo = Column(Float)
    sugars = Column(Integer)
    potass = Column(Integer)
    vitamins = Column(Integer)
    shelf = Column(Integer)
    weight = Column(Float)
    cups = Column(Float)
    rating = Column(Float)

    def __init__(
        self,
        id: Optional[int],
        name: str,
        mfr: str,
        type: Literal["C", "H"],
        calories: int,
        protein: int,
        fat: int,
        sodium: int,
        fiber: float,
        carbo: float,
        sugars: int,
        potass: int,
        vitamins: int,
        shelf: Literal[1, 2, 3],
        weight: float,
        cups: float,
        rating: float,
    ) -> None:
        """Initialize class.

        Args:
            id (int): Id of cereal.
            name (str): Name of cereal.
            mfr (str): Manifacturer.
            type (Literal["C", "H"]): Is cereal eaten hot or cold.
            calories (int): Calories pr serving.
            protein (int): proteins pr serving.
            fat (int): Fat pr serving.
            sodium (int): Sodium pr serving.
            fiber (float): Fiber pr serving.
            carbo (float): Carbohydrates pr serving.
            sugars (int): Sugars pr serving.
            potass (int): Potassium pr serving.
            vitamins (int): Vitamins pr serving.
            shelf (Literal[1, 2, 3]): Display shelf counting from floor.
            weight (float): Weight in ounces of one serving.
            cups (float): Number of cups in one serving.
            rating (float): Rating of the cereals.
        """
        self.id = id
        self.name = name
        self.mfr = mfr
        self.type = type
        self.calories = calories
        self.protein = protein
        self.fat = fat
        self.sodium = sodium
        self.fiber = fiber
        self.carbo = carbo
        self.sugars = sugars
        self.potass = potass
        self.vitamins = vitamins
        self.shelf = shelf
        self.weight = weight
        self.cups = cups
        self.rating = rating

    @staticmethod
    def get_cereal_by_id(db: Session, cereal_id: int) -> Type["Cereal"]:
        """Get cereal by id.

        Returns:
            Cereal: found Cereal.
        """
        cereal = db.query(Cereal).filter(Cereal.id == cereal_id).first()
        db.close()
        if cereal is None:
            raise HTTPException(status_code=404, detail="Cereal not found")
        return cereal  # type:ignore

    @staticmethod
    def get_cereals(
        db: Session,
        field: Optional[str],
        value: Optional[Any],
        operator: Optional[Literal["eq", "lt", "gt"]],
    ) -> list[Type["Cereal"]]:
        """Search for cereal, with optional filtering.

        Args:
            db (Session): Database
            field (Optional[str]): Search filed.
            value (Optional[Any]): Value.
            operator (Optional[Literal["eq", "lt", "gt]]) Operator.

        Returns:
            list[Cereal]: List of found cereal.
        """
        query = db.query(Cereal)

        if field is None:
            results = db.query(Cereal).all()
        elif field not in VALID_FIELDS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid field provided: {field}.",
            )
        else:
            query = db.query(Cereal)
            if value is not None:
                if operator == "eq":
                    query = query.filter(getattr(Cereal, field) == value)
                elif operator == "gt":
                    query = query.filter(getattr(Cereal, field) > value)
                elif operator == "lt":
                    query = query.filter(getattr(Cereal, field) < value)
                else:
                    HTTPException()
            results = query.all()

        if not results:
            raise HTTPException(
                status_code=404,
                detail="No cereals found with the specified criteria",
            )
        return results  # type:ignore


if __name__ == "__main__":
    pass
