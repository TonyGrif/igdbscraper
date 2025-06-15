from pprint import pprint

from igdbscraper import PlatformScraper


def main():
    scraper = PlatformScraper("ps2")
    pprint(scraper.best)
    pprint(scraper.metadata)
    pprint(scraper.subset_games(1, 3, end_inclusive=True))


if __name__ == "__main__":
    main()
