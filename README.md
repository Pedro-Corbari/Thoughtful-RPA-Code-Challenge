# PEDROCORBARI_Thoughtful Challenge

## Description

This project is the solution to the automation challenge proposed by Thoughtful AI. The goal is to create an RPA (Robotic Process Automation) bot using Python and Selenium to extract data from a news website, process it, and store it in an Excel file.

## Features

The bot performs the following tasks:

1. **Open the news website**: The bot accesses the specified URL.
2. **Search for phrases**: It enters a search phrase into the search field.
3. **Filter results**: Filters the results based on the news category and the specified time period.
4. **Data extraction**: Extracts the title, date, description, and image of the latest news that meets the criteria.
5. **Content analysis**: Counts the number of occurrences of the search phrase in the title and description, and checks for the mention of monetary values.
6. **Data storage**: Saves the extracted data in an Excel file, including the image file name and content analysis results.
7. **Image download**: Downloads the images associated with the news and saves them in the output folder.

## Requirements

- **Python 3.8+**
- **Selenium**
- **Pandas**


## Usage

1. **Robocorp Control Room Setup**:
   - Ensure the parameters (search phrase, news category, and number of months) are correctly configured in Robocorp Control Room.

2. **Run the Bot**:
   - The bot can be executed via Robocorp Control Room or directly through the Python code.

3. **Output**:
   - The results will be stored in the `/output` folder, including the Excel file with the data and the downloaded images.

## Project Structure

- `src/`: Contains the main source code.
- `output/`: Directory where the output files are stored.
- `main.py`: Main Python file.
- `README.md`: This file.
