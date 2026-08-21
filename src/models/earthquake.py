from pydantic import BaseModel
from datetime import datetime
class Earthquake(BaseModel):
    mag: float
    place: str
    time: datetime
    tsunami: bool
    sig: int
    ids: str
    nst: int
    rms: float
    coordinates: list[float]


