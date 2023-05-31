import enum
import requests
from bs4 import BeautifulSoup
from pprint import pprint

class WebScraperError(Exception):
    pass

class NetworkError(WebScraperError):
    pass

class ParsingError(WebScraperError):
    pass

HEADERS = {
    'authority': 'flixpatrol.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,la;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': '_nss=1; _ga=GA1.2.1758190770.1677534659; _gid=GA1.2.1944429410.1681412121; _gat_gtag_UA_2491325_22=1',
    'referer': 'https://flixpatrol.com/top10/',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'Windows',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}
URL = 'https://flixpatrol.com/top10/streaming/world/today/full/'
def get_response(url: str):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        raise NetworkError(f"Error fetching URL: {e}")

response = get_response(URL)
print(response.status_code)

class MediaType(enum.Enum):
    MOVIE = 1
    TV = 2

class Platform(enum.Enum):
    NETFLIX = "netflix"
    HULU = "hulu"
    AMAZON_PRIME = "amazon-prime"
    APPLE_TV = "apple-tv"
    DISNEY = "disney"
    PARAMOUNT_PLUS = "paramount-plus"
    HBO = "hbo"

def get_titles(platform: Platform, media_type: MediaType, content: bytes) -> dict:
    # Check if the specified platform and media type are valid
    if not isinstance(media_type, MediaType):
        raise ValueError("Invalid media type")
    if not isinstance(platform, Platform):
        raise ValueError("Invalid platform")

    try:
        soup = BeautifulSoup(content, "html.parser")
    except Exception as e:
        raise ParsingError(f"Error parsing HTML content: {e}")

    # Find the div with specified ID
    div = soup.find('div', {'id': f"{platform.value}-{media_type.value}"})

    # Create a dictionary to store the titles
    titles = {}

    # Extract the title from the list
    if div:
        title_list = div.find_all(['a', 'h3'])  # Search for both 'a' and 'h3' tags
        for index, title_elem in enumerate(title_list, start=1):
            title = title_elem.text
            # Skip the first two titles
            if index > 2:
                titles[index - 2] = title  # Subtract 2 from index to start from 1 to exclude some none titles
    print("got titles")
    return titles

def get_platform(platform: Platform):
    movie_titles = get_titles(platform, MediaType.MOVIE, response.content)
    tv_titles = get_titles(platform, MediaType.TV, response.content)

    platform_titles = {
        "movies": {rank: {"title": title} for rank, title in movie_titles.items()},
        "tv_shows": {rank: {"title": title} for rank, title in tv_titles.items()}
    }
    print("got platform")
    return platform_titles

def get_all_platforms():
    platforms = list(Platform)
    all_platforms = {platform.value: get_platform(platform) for platform in platforms}
    print("got all platforms")
    return all_platforms
