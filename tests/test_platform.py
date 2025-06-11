import pytest

from igdbscraper import PlatformScraper


@pytest.fixture
def scraper():
    return PlatformScraper("ps2")


class TestPlatformScraper:
    def test_scrape_metadata(self, scraper):
        data = scraper.metadata
        assert data.name == "PlayStation 2"
        assert data.description is not None
        assert data.manufacturer_id == 45
        assert data.developers_id == 45
        assert data.generation == "Sixth generation"
        assert data.platform_type == "Console"
        assert data.product_family == "PlayStation"
        assert data.alt_name == "PS2"
        assert len(data.release_dates) == 5
        assert len(data.introduction_price) == 6

    def test_scrape_hardware_metadata(self, scraper):
        hardware = scraper.metadata.hardware
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

    def test_scrape_other_versions(self, scraper):
        versions = scraper.metadata.other_versions
        assert len(versions) == 1
        assert versions[0].name == "Slimline"
        assert versions[0].description is not None
        assert versions[0].link is not None

    def test_scrape_bestgames(self, scraper):
        best = scraper.best
        assert len(best) == 100
        assert best[6].title == "Metal Gear Solid 2: Sons of Liberty"

        top = best[0]
        assert top.title == "Metal Gear Solid 3: Snake Eater"
        assert top.year == 2004
        assert top.rank == 1
        assert top.score == 92
        assert top.id == 379
        assert top.link is not None

    def test_scrape_games(self, scraper):
        games = scraper.games(start=249, end=251, end_inclusive=True)
        assert len(games) == 30

        game = games[11]
        assert game.title == "Persona 3"
        assert game.year == 2006
        assert game.link is not None
