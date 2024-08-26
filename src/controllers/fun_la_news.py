"""Functions for la_news_scrap"""
from datetime import datetime, timedelta
from dataclasses import asdict
import pandas
from src.models.la_news_models import News

class la_news_functions:
    """Useful functions for verify dates in range"""

    def parse_date(self, input_date: str) -> datetime:
        """Parses a date string in either 'MMM. DD, YYYY' or 'MMMM DD, YYYY' format."""
        try:
            return datetime.strptime(input_date, "%b. %d, %Y")
        except ValueError:
            return datetime.strptime(input_date, "%B %d, %Y")

    def is_date_in_range(self, months: int, input_date: str) -> bool:
        """Checks if the input date is within the specified number of months from today."""
        current_date = datetime.today()
        input_date = self.parse_date(input_date)

        if months == 0:
            return input_date.year == current_date.year and input_date.month == current_date.month

        start_date = current_date - timedelta(days=months * 30)
        return start_date <= input_date <= current_date

class csv_generator:
    """Generate the csv with the business logical"""    
    def __init__(self, logger, csv_name) -> None:
        self.logger = logger
        self.csv_name = csv_name

    def generate_csv(self, data: list[News]):
        """Generate the csv with the result scraping"""   
        try:
            self.logger.info('Creating CSV')
            df = pandas.DataFrame([asdict(news) for news in data])
            df.to_csv(f'output//{self.csv_name}.csv', index=False, encoding="utf-8-sig", sep=";")
            self.logger.info('CSV created successfully')
        except Exception as e:
            self.logger.error(f"Unexpected error: {type(e).__name__} - {e}")
