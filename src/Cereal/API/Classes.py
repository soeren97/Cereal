"""Class to handle API objects."""

from pydantic import BaseModel


class APICereal(BaseModel):
    """Model representing the data structure."""

    name: str
    manufacturer: str
    type: str
    calories: int
    protein: int
    fat: int
    sodium: int
    fiber: float
    carbo: float
    sugars: int
    potassium: int
    vitamins: int
    shelf: int
    weight: float
    cups: float
    rating: float

    class Config:
        """Configurations."""

        from_attributes = True
