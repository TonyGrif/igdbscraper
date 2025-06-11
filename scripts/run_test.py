from pprint import pprint

from igdbscraper import PlatformScraper


def main():
    scraper = PlatformScraper("ps2")
    # pprint(scraper.url)
    # pprint(scraper.best)
    # pprint(scraper.metadata)
    pprint(scraper.games(7, 9))


if __name__ == "__main__":
    main()
