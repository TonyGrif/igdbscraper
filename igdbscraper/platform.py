"""This module contains methods to scrape platform data"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class PlatformHardware:
    """This class stores information on the platform's hardware"""

    operating_system: str
    cpu: str
    memory: str
    storage: List  # TODO: Pretty sure I need to init this
    graphics: str
    sound: str
    online_service: str
    output: List  # TODO: Pretty sure I need to init this
    supported_resolutions: List  # TODO: Pretty sure I need to init this
    connectivity: List  # TODO: Pretty sure I need to init this


@dataclass
class PlatformMeta:
    """This class stores information about the platform itself"""

    name: str
    description: str
    release_dates: List  # TODO: Pretty sure I need to init this
    manufacturer_id: int
    developers_id: int
    generation: str
    platform_type: str
    product_family: str
    introduction_price: Dict  # TODO: Pretty sure I need to init this
    alt_name: str
    hardware: PlatformHardware
    other_versions: List  # TODO: Pretty sure I need to init this, may also skip this


class PlatformScraper:
    """This class is used to scrape platform information

    Attributes:
        meta: dataclass storing meta information about the console
        games: full list of games from this platform
        best: IGDB's top 100 games from this platform
    """

    def __init__(self) -> None:
        """Constructor for the PlatformScraper"""
        self.meta = None
        self.games = None
        self.best = None

    async def scrape_metadata(self) -> None:
        raise NotImplementedError

    async def scrape_games(self) -> None:
        raise NotImplementedError

    async def scrape_best_games(self) -> None:
        raise NotImplementedError
