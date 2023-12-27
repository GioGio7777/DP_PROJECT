# Importing necessary modules and classes
from __future__ import annotations
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsel import Selector
from abc import ABC, abstractmethod

# URLs for scraping
URL_MATCH = "https://www.livescore.in/tr/futbol/turkiye/super-li-g/#/KzRFDJ4U/table/overall"
URL_LOL = "https://www.op.gg/summoners"


# Context class that maintains a reference to a strategy
class Context():
    """
    The Context defines the interface of interest to clients.
    """

    def __init__(self, strategy: Strategy):
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        """
        The Context maintains a reference to one of the Strategy objects.
        The Context does not know the concrete class of a strategy.
        It should work with all strategies via the Strategy interface.
        """
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def run_scrap(self, values,*args):
        # Setting up a headless Firefox browser
        options = Options()
        options.headless = True
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)

        # Using the current strategy to get information
        value,url = self._strategy.getInformation(values, self.driver,*args)

        # Returning the scraped information
        return value,url


# Abstract Strategy class with a common interface
class Strategy(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """

    @abstractmethod
    def getInformation(self, values, driver,*args):
        pass


# Concrete strategy class for scraping League of Legends (LoL) information
class RiotScrapper(Strategy):
    def getInformation(self, values, driver,*args):
        # Constructing the URL for LoL information

        if len(args) == 1:
            url = URL_LOL + "/" + args[0].lower() + "/" + values
        elif len(args) == 2:
            url = URL_LOL + "/" + args[0].lower() + "/" + values +"-"+args[1]
        else:
            return

        # Opening the URL in the browser
        driver.get(url)

        # Waiting for the presence of the content element
        (WebDriverWait(driver, 5)
         .until(EC.presence_of_element_located((By.CLASS_NAME, 'content'))))

        # Using parsel to parse the HTML page
        sel = Selector(text=driver.page_source)

        # Extracting specific information from the page
        parsed = [{
            'user': values,
            'server': args[0],
            'rank': driver.find_element(By.XPATH,
                                        "//div[contains(@class,'css-1kw4425 ecc8cxr0')]/div[contains(@class,content)]/div[contains(@class,info)]//div[contains(@class,tier)]").get_attribute(
                "innerHTML").replace("<!-- -->", ""),
            'win': driver.find_element(By.XPATH,
                                       "//div[contains(@class,'win-lose-container')]//div[contains(@class,'win-lose')]").get_attribute(
                "innerHTML").split(" ")[0].replace("<!--", "").replace("W", ""),

            'win-rate':
                driver.find_element(By.XPATH, "//div[contains(@class,'ratio')]").get_attribute("innerHTML").split(
                    " ")[4].replace("-->", "").replace("<!--", "").replace("L", ""),
            "profile_img":
                driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div[1]/div/div[1]/div[1]/img").get_attribute(
                    "src"),
            "rank_img":
                driver.find_element(By.XPATH,
                                    "//*[@id='content-container']/div[1]/div[1]/div[2]/div[1]/img").get_attribute('src')
        }]

        # Closing the browser
        driver.quit()
        return parsed,url


# Concrete strategy class for scraping match information
class MatchScrapper(Strategy):
    def getInformation(self, values, driver):
        # Opening the specified URL in the browser
        driver.get(values)

        # Waiting for the presence of the ui-table__body element
        element = (WebDriverWait(driver, 5)
                   .until(EC.presence_of_element_located((By.CLASS_NAME, 'ui-table__body'))))

        # Using parsel to parse the HTML page
        sel = Selector(text=driver.page_source.replace("<!--", "").replace("-->", ""))
        parsed = []

        # Extracting match information from each ui-table__row
        for item in sel.xpath("//div[contains(@class, 'ui-table__row')]"):
            parsed.append({
                'rank': item.css('div::text').get(),
                'team': item.css('a::text').get(),
                'Match': item.xpath("//span[contains(@class,' table__cell table__cell--value')]").css(
                    'span::text').get(),
                'Win': item.css('span::text')[1].get(),
                'Draw': item.css('span::text')[2].get(),
                'Lose': item.css('span::text')[3].get(),
                'Point': item.css('span::text')[6].get(),
                'Average': item.css('span::text')[5].get(),
            })

        # Closing the browser
        driver.quit()
        return parsed,values


# Main execution block
if __name__ == "__main__":
    # Creating a Context object with the RiotScrapper strategy
    context = Context(RiotScrapper())

    # Running the scrape for LoL information
    lol = context.run_scrap("EUNE-JodίoJoestar")
    print(lol)

    ## Uncomment the following lines to test MatchScrapper strategy
    # context.strategy = MatchScrapper()
    # matches = context.run_scrap(URL_MATCH)
    # print(matches)
