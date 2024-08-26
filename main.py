"""Main file"""
from robocorp import workitems
from src.controllers.la_news_scrap import Lanews
from src.setup import Config
from src.controllers.fun_la_news import csv_generator


def main():
    """Main function"""
    CSV_NAME = "report"
    config = Config()
    la_times_scrapper = Lanews(config)
    for item in workitems.inputs:
        phrase = item.payload["phrase"]
        category = item.payload["category"]
        months_number = item.payload["months_number"]
        type_news = item.payload["type_news"]
        news = la_times_scrapper.run(
            phrase,
            category,
            months_number,
            type_news
        )
        csv_generator(config.logger, CSV_NAME).generate_csv(news)

if __name__ == '__main__':
    main()
