"""This module contains methods to scrape platform data"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, no_type_check

import httpx
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

_IGDB_URL = "https://www.igdb.com"


@dataclass
class PlatformHardware:
    """This class stores information on the platform's hardware"""

    operating_system: str
    cpu: str
    memory: str
    graphics: str
    sound: str
    online_service: str

    storage: List[str] = field(default_factory=list)
    output: List[str] = field(default_factory=list)
    supported_resolutions: List[str] = field(default_factory=list)
    connectivity: List[str] = field(default_factory=list)


@dataclass
class PlatformVersion:
    """This class store information pertaining to a unique version of the console"""

    name: str
    description: str
    link: str  # Included as specific information on it would require another request


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

    hardware: PlatformHardware

    release_dates: List[str] = field(default_factory=list)
    introduction_price: List[str] = field(default_factory=list)
    other_versions: List[PlatformVersion] = field(default_factory=list)


class PlatformScraper:
    """This class is used to scrape platform information

    Attributes:
        url: IGDB link to the platform
        metadata: dataclass storing meta information about the console
        games: full list of games from this platform
        best: IGDB's top 100 games from this platform
    """

    def __init__(self, platform: str) -> None:
        """Constructor for the PlatformScraper

        Args:
            platform: the name of the console to append to the URL
        """
        self._url = f"{_IGDB_URL}/platforms/{platform}"

        self._metadata: Optional[PlatformMeta] = None
        self.games = None
        self.best = None

    @property
    def url(self) -> str:
        """Return the platform's link"""
        return self._url

    @property
    def metadata(self) -> PlatformMeta:
        """Return the platform's metadata"""
        if self._metadata is not None:
            return self._metadata

        res = self._request_meta()
        self._metadata = PlatformMeta(**self._parse_meta(res))
        return self._metadata

    def _request_meta(self, timeout: int = 5) -> str:
        """Make request on metadata"""
        ua = UserAgent()
        headers = {"User-Agent": ua.random, "Refer": "https://www.google.com/"}

        res = httpx.get(self.url, headers=headers, timeout=timeout)
        res.raise_for_status()
        return res.text

    @no_type_check
    def _parse_meta(self, text: str) -> Dict:
        soup = BeautifulSoup(text, "html.parser")
        data = {}

        data["name"] = soup.find("h1").text.rsplit(" ", 1)[0]
        data["description"] = soup.find("div", {"class": "charlimit"}).text

        ids = soup.find_all("div", {"class": "block"})
        data["manufacturer_id"] = int(ids[0].text)
        data["developers_id"] = int(ids[1].text)

        dates = soup.find("div", {"class": "col-sm-4 col-xs-6"}).find_all(
            "div", {"class": "text-muted"}
        )
        data["release_dates"] = [date.text for date in dates]

        information = soup.find_all("div", {"class": "col-md-3 col-sm-4 col-xs-6"})
        data["generation"] = information[0].find("a").text
        data["platform_type"] = information[1].find("a").text
        data["product_family"] = information[2].find("a").text
        data["introduction_price"] = [
            info.text for info in information[3].find_all("dd")
        ]
        data["alt_name"] = information[4].find("div").text
        data["hardware"] = PlatformHardware(
            **self._parse_hardware_block(soup.find("div", {"id": "platform-hardware"}))
        )

        version_block = soup.find_all("div", {"class": "panel"})[2].find_all(
            "div", {"class": "media overflow"}
        )
        data["other_versions"] = [
            self._parse_version_block(version) for version in version_block
        ]

        return data

    @no_type_check
    def _parse_hardware_block(self, soup) -> Dict:
        data = {}
        table = soup.find_all("tr")

        data["operating_system"] = table[0].find_all("td")[0].text
        data["cpu"] = table[0].find_all("td")[1].text

        data["memory"] = table[1].find_all("td")[0].text
        data["storage"] = table[1].find_all("td")[1].text.split(", ")

        data["graphics"] = table[2].find_all("td")[0].text
        data["sound"] = table[2].find_all("td")[1].text

        data["online_service"] = table[3].find_all("td")[0].text
        data["output"] = table[3].find_all("td")[1].text.split(", ")

        data["supported_resolutions"] = table[4].find_all("td")[0].text.split(", ")
        data["connectivity"] = table[4].find_all("td")[1].text.split(", ")

        return data

    @no_type_check
    def _parse_version_block(self, soup) -> PlatformVersion:
        data = {}

        data["name"] = soup.find_all("a")[1].text
        data["link"] = f"{_IGDB_URL}/{soup.find_all('a')[1]['href']}"

        soup.find("h4").decompose()
        data["description"] = soup.text

        return PlatformVersion(**data)
