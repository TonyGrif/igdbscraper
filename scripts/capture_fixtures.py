"""Refresh the mock-test HTML fixtures from the live IGDB site"""

from pathlib import Path

from igdbscraper import PlatformScraper

_FIXTURES = Path(__file__).parent.parent / "tests" / "fixtures"


def _capture(scraper: PlatformScraper, url: str, filename: str) -> None:
    scraper.create_driver()
    scraper._driver.get(url)
    import time

    time.sleep(scraper._sleep)
    (_FIXTURES / filename).write_text(scraper._driver.page_source, encoding="utf-8")
    scraper.quit_driver()


def main() -> None:
    scraper = PlatformScraper("ps2", sleep=3)
    _FIXTURES.mkdir(parents=True, exist_ok=True)

    _capture(scraper, scraper.url, "platform_meta.html")
    _capture(scraper, scraper.best_url, "platform_best.html")
    _capture(scraper, f"{scraper.url}/games?title=asc&page=150", "platform_games.html")


if __name__ == "__main__":
    main()
