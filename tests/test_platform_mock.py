from pathlib import Path

import pytest

from igdbscraper import PlatformScraper

_FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def scraper():
    return PlatformScraper("ps2")


@pytest.fixture
def meta_html():
    return (_FIXTURES / "platform_meta.html").read_text()


@pytest.fixture
def best_html():
    return (_FIXTURES / "platform_best.html").read_text()


@pytest.fixture
def games_html():
    return (_FIXTURES / "platform_games.html").read_text()


class TestPlatformScraperMock:
    """Parsing tests against saved HTML fixtures (no network/browser)"""

    def test_parse_metadata(self, scraper, meta_html):
        data = scraper._parse_meta(meta_html)
        assert data["name"] == "PlayStation 2"
        assert data["description"] is not None
        assert data["generation"] == "Sixth generation"
        assert data["platform_type"] == "Console"
        assert data["product_family"] == "PlayStation"
        assert data["alt_name"] == "PS2"
        assert len(data["release_dates"]) == 5
        assert len(data["introduction_price"]) == 6

    def test_parse_hardware_metadata(self, scraper, meta_html):
        hardware = scraper._parse_meta(meta_html)["hardware"]
        assert hardware.operating_system == ""
        assert hardware.cpu == "Emotion Engine @ 294.912 MHz"
        assert hardware.memory == "32 MB"
        assert hardware.graphics == "Graphics Synthesizer @ 147.456 MHz"
        assert hardware.sound == "CPU+SPU2"
        assert hardware.online_service == "Dynamic Network Authentication System"
        assert len(hardware.storage) == 2
        assert len(hardware.output) == 5
        assert len(hardware.supported_resolutions) == 2
        assert len(hardware.connectivity) == 2

    def test_parse_other_versions(self, scraper, meta_html):
        versions = scraper._parse_meta(meta_html)["other_versions"]
        assert len(versions) == 1
        assert versions[0].name == "Slimline"
        assert versions[0].description is not None
        assert versions[0].link is not None

    def test_parse_bestgames(self, scraper, best_html):
        best = scraper._parse_best_games(best_html)
        assert len(best) == 100

        top = best[0]
        assert top.title == "Metal Gear Solid 3: Snake Eater"
        assert top.year == 2004
        assert top.rank == 1
        assert top.score == 9.3
        assert top.id == 379
        assert top.link is not None

    def test_parse_games(self, scraper, games_html):
        games = scraper._parse_games(games_html)
        assert len(games) == 10

        game = games[1]
        assert game.title == "Heroes of the Pacific"
        assert game.year == 2005
        assert game.link is not None
        assert "PlayStation 2" in game.platforms
