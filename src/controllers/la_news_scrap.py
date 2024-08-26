"""Main scrap file for Thoughtful RPA Coding Challenge"""
import os
import time
import imghdr
import wget
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from src.constants.la_times_constants import LATimesConstants
from src.models.la_news_models import News
from src.controllers.fun_la_news import la_news_functions
from src.setup import Config


class Lanews:
    """LA news bot"""


    def __init__(self, config: Config) -> None:
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1400,608")
        self.url = LATimesConstants.URL
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(1400,608)
        self.timeout = LATimesConstants.TIMEOUT_BROWSER
        self.wait = WebDriverWait(self.driver, self.timeout)
        self.config = config
        self.logger = config.logger

    def download_image(self, news, news_counter) -> str:
        """Download the news imagem by url using wget library and return news name"""
        self.logger.info(f"Downloading image from news {news_counter}")
        img = news.find_element(By.XPATH, LATimesConstants.XP_PIC_URL)
        url = img.get_attribute("src")
        temp_name = f"news_{news_counter}"
        path_temp = f"output//{temp_name}"
        wget.download(url, path_temp)
        image_type = imghdr.what(path_temp)
        if not image_type:
            raise ValueError("Could not infer the image type.")

        new_file_name = f'{temp_name}.{image_type}'
        new_file_path = os.path.join("output//", new_file_name)

        os.rename(path_temp, new_file_path)
        return new_file_name

    def web_interact(self, locator, path, interact, input_int=None, timeout=10) -> None:
        """Interacts with a web element based on the specified locator and action."""
        time.sleep(4)
        actions = {
            ("XP", "input"): (By.XPATH, lambda e: e.send_keys(input_int)),
            ("CS", "input"): (By.CSS_SELECTOR, lambda e: e.send_keys(input_int)),
            ("XP", "click"): (By.XPATH, lambda e: e.click()),
            ("CS", "click"): (By.CSS_SELECTOR, lambda e: e.click())
        }

        by, action = actions.get((locator, interact))
        if not by:
            raise ValueError(f"Unsupported locator ({locator}) or interaction ({interact}).")

        # Retry mechanism to handle StaleElementReferenceException
        for attempt in range(3):
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located((by, path))
                )
                action(element)
                break
            except StaleElementReferenceException:
                if attempt < 2:
                    continue
                else:
                    raise
            except TimeoutException:
                pass

    def close_shadow_element(self, xp_parent, sl_close_ad, timeout=10) -> None:
        """Close shadow root"""
        try:
            self.logger.info('Closing shadow element (ad)')
            parent_element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xp_parent))
            )
            shadow_root = parent_element.shadow_root
            time.sleep(1)

            WebDriverWait(shadow_root, timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, sl_close_ad))
            )
            shadow_parent = self.driver.find_element(By.XPATH, xp_parent).shadow_root
            shadow_parent.find_element(By.CSS_SELECTOR, sl_close_ad).click()
        except Exception as e:
            self.logger.error(f"Could not close ad: {e}")

    def _expand_element(self, xpath):
        """Expand a collapsible element using ActionChains."""
        self.logger.debug(f'Expanding element with XPath: {xpath}')
        elem = self.driver.find_element(By.XPATH, xpath)
        actions = ActionChains(self.driver)
        actions.move_to_element(elem).click().perform()

    def run(self, phrase_scrap, category_run, months_number_scrap, type_news) -> None:
        """Call functions and control flow"""
        try:
            self.logger.info(f'Starting flow {self.url}')
            self.start_web(self.url)
            self.search(phrase_scrap)
            self.filter_topics(category_run, type_news)
            news = self.get_news(phrase_scrap, months_number_scrap)
            return news
        except Exception as error:
            self.logger.error(f"Unexpected error: {type(error).__name__} - {error}")
        finally:
            self.driver.close()

    def start_web(self, url) -> None:
        "Start browser"
        self.logger.info('Starting browser')
        time.sleep(1)
        self.driver.get(url)

    def search(self, phrase_run) -> None:
        """Search the phrase and select newest"""
        self.logger.info('Starting searching process interactions with web')
        self.web_interact("XP", LATimesConstants.XP_SEARCH_INPUT, "click")
        self.web_interact("XP", LATimesConstants.XP_SEARCH_INPUT, "input", phrase_run)
        self.web_interact("XP", LATimesConstants.XP_SEARCH_BUTTON, "click")
        self.web_interact("XP", LATimesConstants.XP_NEWEST_BUTTON, "click")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.close_shadow_element(
            LATimesConstants.SR_XP_PARENT,
            LATimesConstants.SR_CS_CLOSE_AD,
            timeout=20
            )
        self._expand_element(LATimesConstants.XP_TOPIC_EXPAND)
        self._expand_element(LATimesConstants.XP_TYPE_EXPAND)

    def filter_topics(self, category, type_news) -> None:
        """Filter interactions with the browser"""
        self.logger.info('Starting filtering process')
        cat_table = self.driver.find_elements(By.XPATH, LATimesConstants.XP_CATEGORIES_TABLE)

        # Both for loops was to make a different click using javascript script
        for cat in cat_table:
            self.logger.info(category.lower())
            self.logger.info(cat.text.lower())
            if category.lower() in cat.text.lower():
                spn_cat = cat.find_element(By.XPATH, LATimesConstants.XP_SPAN_CAT)
                self.driver.execute_script("arguments[0].click();", spn_cat)
                break
        time.sleep(1)
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, LATimesConstants.XP_TYPE_TABLE))
        )

        type_table = self.driver.find_elements(By.XPATH, LATimesConstants.XP_TYPE_TABLE)
        for typ in type_table:
            if type_news.lower() in typ.text.lower():
                spn_type = typ.find_element(By.XPATH, LATimesConstants.XP_SPAN_TYPE)
                self.driver.execute_script("arguments[0].click();", spn_type)
                break
        time.sleep(3)

    def get_news(self, phrase_scrap, months_numbers) -> list:
        """Scrap the news on conditional rules"""
        self.logger.info('scraping news')
        news: list[News] = []
        report_table = self.driver.find_elements(By.XPATH, LATimesConstants.XP_NEWS_TABLE)
        report_counter = 1
        for report in report_table:
            news_title = report.find_element(By.XPATH, LATimesConstants.XP_NEWS_TITLE).text
            news_desc = report.find_element(By.XPATH, LATimesConstants.XP_NEWS_DESC).text
            news_date = report.find_element(By.XPATH, LATimesConstants.XP_NEWS_DATE).text
            img_name = self.download_image(report, report_counter)
            news.append(News(
                title=news_title,
                description=news_desc,
                date=news_date,
                search_phrase=phrase_scrap,
                image=img_name
            ))
            report_counter += 1
            datarange_news = la_news_functions().is_date_in_range(months_numbers, news_date)
            if not datarange_news:
                break
        return news
