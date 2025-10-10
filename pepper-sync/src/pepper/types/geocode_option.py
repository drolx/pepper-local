from typing import Annotated, Literal, Optional

from annotated_types import Gt
from pydantic import BaseModel


class GeocodeOption(BaseModel):
    enable: bool = False
    type: Optional[Literal["nominatim", "pelias", "photon"]] = "nominatim"
    url: Optional[str] = "https://nominatim.openstreetmap.org"
    zoom: Optional[Annotated[int, Gt(4)]] = 15
