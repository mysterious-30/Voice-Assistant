from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def get_driver(proxy=None):
    # Set up Selenium WebDriver with optional proxy
    options = Options()
    options.add_argument("--headless")  # Run headless
    options.add_argument("--disable-gpu")  # Disable GPU acceleration (for headless)
    
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')
    
    # You can specify the path to chromedriver if it's not in PATH
    driver = webdriver.Chrome(options=options)
    return driver


class SearchResult:
    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description

    def __repr__(self):
        return f"SearchResult(url={self.url}, title={self.title}, description={self.description})"


def search(term, num_results=5, lang="en", proxy=None, advanced=False, sleep_interval=5, safe="active", ssl_verify=None, region=None, start_num=0, unique=False):
    """Search the Bing search engine using Selenium to render JavaScript."""

    # Start Selenium WebDriver
    driver = get_driver(proxy)

    fetched_results = 0  # Keep track of the total fetched results
    fetched_links = set()  # to keep track of links that are already seen previously
    start = start_num
    url = f"https://www.bing.com/search?q={term}&count={num_results + 2}&setlang={lang}&first={start}"

    driver.get(url)
 
    while fetched_results < num_results:
        sleep(sleep_interval)  # Optional: To avoid triggering rate-limiting
        
        # Get the page source after JavaScript is rendered
        soup = BeautifulSoup(driver.page_source, "html.parser")
        result_block = soup.find_all("li", attrs={"class": "b_algo"})  # Bing results are within <li class="b_algo">
        new_results = 0  # Keep track of new results in this iteration

        for result in result_block:
            # Find link, title, description
            link = result.find("a", href=True)
            title = result.find("h2")
            description_box = result.find("p")

            if link and title and description_box:
                link = result.find("a", href=True)
                if link["href"] in fetched_links and unique:
                    continue
                fetched_links.add(link["href"])
                description = description_box.text
                fetched_results += 1
                new_results += 1
                if advanced:
                    yield SearchResult(link["href"], title.text, description)
                else:
                    yield link["href"]

            if fetched_results >= num_results:
                break  # Stop if we have fetched the desired number of results

        if new_results == 0:
            # If no new results were found in this iteration
            break

        start += 10  # Prepare for the next set of results
        driver.get(f"{url}&first={start}")

    driver.quit()  # Close the WebDriver after the search is done
