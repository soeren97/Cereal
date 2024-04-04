"""Class to handle API objects."""

from typing import Optional

from pydantic import BaseModel


class APICereal(BaseModel):
    """Model representing the data structure."""

    id: Optional[int]
    name: str
    mfr: str
    type: str
    calories: int
    protein: int
    fat: int
    sodium: int
    fiber: float
    carbo: float
    sugars: int
    potass: int
    vitamins: int
    shelf: int
    weight: float
    cups: float
    rating: float

    class Config:
        """Configurations."""

        from_attributes = True
