"""Assets and locators"""
from dataclasses import dataclass

@dataclass
class LATimesConstants:
    """
    XP = XPATH locators,
    CS = CSS selectors locators,
    SR = Shadow Root elements
    """

    URL = 'https://www.latimes.com/search?q='
    TIMEOUT_BROWSER = 60
    XP_SEARCH_INPUT = "/html/body/div[2]/ps-search-results-module/form/div[1]/input"
    XP_SEARCH_BUTTON = "/html/body/div[2]/ps-search-results-module/form/div[1]/button"
    XP_NEWEST_BUTTON = "/html/body/div[2]/ps-search-results-module/form" \
                    "/div[2]/ps-search-filters/div/main/div[1]/div[2]/div/label/select/option[2]"
    XP_TOPIC_EXPAND = "/html/body/div[2]/ps-search-results-module/form/div[2]/" \
                      "ps-search-filters/div/aside/div/div[3]/div[1]/ps-toggler/" \
                       "ps-toggler/button/span[1]"
    XP_TYPE_EXPAND = "/html/body/div[2]/ps-search-results-module/form/div[2]/" \
                     "ps-search-filters/div/aside/div/div[3]/div[2]/ps-toggler/" \
                     "ps-toggler/button/span[1]"
    SR_XP_PARENT = "/html/body/modality-custom-element"
    SR_CS_CLOSE_AD = "#icon-close-greylt"
    XP_CATEGORIES_TABLE = "/html/body/div[2]/ps-search-results-module" \
                       "/form/div[2]/ps-search-filters/div/aside/div" \
                       "/div[3]/div[1]/ps-toggler/ps-toggler/div/ul/li"
    XP_SPAN_CAT = "./div/div[1]/label/span"
    XP_TYPE_TABLE = "/html/body/div[2]/ps-search-results-module/" \
                       "form/div[2]/ps-search-filters/div/aside/div" \
                       "/div[3]/div[2]/ps-toggler/ps-toggler/div/ul/li"
    XP_SPAN_TYPE = "./div/div[1]/label/span"
    XP_NEWS_TABLE = "/html/body/div[2]/ps-search-results-module/form/" \
                    "div[2]/ps-search-filters/div/main/ul/li"
    XP_PIC_URL = "./ps-promo/div/div[1]/a/picture/img"
    XP_NEWS_TITLE = "./ps-promo/div/div[2]/div/h3/a"
    XP_NEWS_DESC = "./ps-promo/div/div[2]/p[1]"
    XP_NEWS_DATE = "./ps-promo/div/div[2]/p[2]"
