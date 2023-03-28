from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)
log_file = "scraper.log"
log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)

service_list = ["netflix", "amazon-prime", "hbo", "hulu", "disney", "paramount-plus"]
class FlixPatrolScraper:
    def __init__(self, services):
        self.services = services

        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(options=chrome_options)

    def scrape_top_ten_movies(self, service):
        url = "https://flixpatrol.com/top10/"
        self.driver.get(url)

        try:
            # Wait for the top 10 section to appear
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, f"{service}-1")))

            # Scrape the top 10 movies
            top_ten = self.driver.find_element(By.ID, f"{service}-1").find_element(By.CLASS_NAME, "tabular-nums")
            links = top_ten.find_elements(By.TAG_NAME, "a")

            movie_list = []
            for link in links:
                divs = link.find_elements(By.TAG_NAME, "div")
                movie_list.append({"title": f"{divs[2].text}", "year": "null"})

            return movie_list

        except Exception as e:
            # Log the error with the ERROR level
            logger.error(f"Scraping error: {str(e)}")
            
            # Raise an exception with a user-friendly error message
            raise ValueError(f"Failed to scrape top 10 movies for service: {service}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

