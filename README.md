# IGDB Scraper
A Python web scraper for the [IGDB](https://www.igdb.com/) website.

> [!NOTE]
> Before using, check the IGDB API to see if that will fit your needs; this project
> will not implement features already present in the API.

## Usage
```py
from igdbpyscraper import PlatformScraper

scraper = PlatformScraper("{PLATFORM}")
print(scraper.metadata) # Print platform metadata
```

## Authors
* [TonyGrif](https://github.com/TonyGrif) - Creator and Maintainer

## License
This project is licensed under the MIT License
