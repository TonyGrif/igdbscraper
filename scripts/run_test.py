from pprint import pprint

from igdbscraper import PlatformScraper


def main():
    scraper = PlatformScraper("ps2")
    pprint(scraper.url)
    pprint(scraper.best)
    pprint(scraper.metadata)


if __name__ == "__main__":
    main()
