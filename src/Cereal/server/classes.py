"""SQL schema."""

from typing import Literal

from sqlalchemy import Column, Enum, Float, Integer, String

from Cereal.constants import Base


class Cereal(Base):
    """Cereal entity in Cereal database."""

    __tablename__ = "cereal"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    mfr = Column(Enum("A", "G", "K", "N", "P", "Q", "R", name="manifacturer"))
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
        id: int,
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


if __name__ == "__main__":
    pass
