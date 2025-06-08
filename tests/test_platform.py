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

    def test_scrape_games(self, scraper):
        assert False

    def test_scrape_bestgames(self, scraper):
        assert False
