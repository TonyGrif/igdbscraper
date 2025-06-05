"""This module contains methods to scrape platform data"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import httpx
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from loguru import logger


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
    manufacturer_id: int
    developers_id: int
    generation: str
    platform_type: str
    product_family: str
    alt_name: str

    # hardware: PlatformHardware

    release_dates: List[str] = field(default_factory=list)
    introduction_price: Dict = field(default_factory=dict)
    other_versions: List = field(default_factory=list)


class PlatformScraper:
    """This class is used to scrape platform information

    Attributes:
        metadata: dataclass storing meta information about the console
        games: full list of games from this platform
        best: IGDB's top 100 games from this platform
    """

    def __init__(self, platform: str) -> None:
        """Constructor for the PlatformScraper

        Args:
            platform: the name of the console to append to the URL
        """
        self._url = f"https://www.igdb.com/platforms/{platform}"

        self._metadata: Optional[PlatformMeta] = None
        self.games = None
        self.best = None

    @property
    def metadata(self) -> PlatformMeta:
        """Return the platform's metadata"""
        if self._metadata is not None:
            return self._metadata

        res = self._request_meta()
        self._metadata = PlatformMeta(*self._parse_meta(res))
        return self._metadata

    def _request_meta(self, timeout: int = 5) -> str:
        """Make request on metadata"""
        ua = UserAgent()
        headers = {"User-Agent": ua.random, "Refer": "https://www.google.com/"}

        res = httpx.get(self._url, headers=headers, timeout=timeout)
        res.raise_for_status()
        return res.text

    def _parse_meta(self, text: str) -> Dict:
        soup = BeautifulSoup(text, "html.parser")
        return {}
