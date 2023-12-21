# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time, csv
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By

# chrome_options = Options()
# chrome_options.add_argument("--ignore-ssl-errors=yes")
# chrome_options.add_argument("--ignore-certificate-errors")

# driver = webdriver.Chrome(options=chrome_options)

# # Navigate to the webpage
# driver.get("https://search.espncricinfo.com/ci/content/site/search.html")

# # Wait for the page to load
# time.sleep(
#     5
# )  # This is a simple way to wait, but you might want to use more sophisticated methods

# search_input = driver.find_element(
#     By.XPATH, '//*[@id="primary-search"]/div/div/input[1]'
# )

# # Type the search query into the input field
# player_query = "travis head"
# search_input.send_keys(player_query)

# # Optional: Submit the search by sending Enter keypress (if there's no separate search button)
# search_input.send_keys(Keys.ENTER)

# # driver.implicitly_wait(30)
# search_result = driver.find_element(
#     By.XPATH, '//*[@id="viewport"]/div[5]/div[2]/main/div/div[4]/ul/li'
# )

# # Find the link within the search result
# link = search_result.find_element(By.TAG_NAME, "a").get_attribute("href")

# # Navigate to the URL found in the href attribute
# driver.get(link)


# # Function to extract T20 stats from a given table
# def extract_t20_stats(table):
#     rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
#     for row in rows:
#         first_cell_text = row.find_element(By.CSS_SELECTOR, "td").text
#         if "T20s" in first_cell_text:
#             return [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
#     return []


# # Locate the batting & fielding stats table and extract T20 stats
# batting_fielding_table = driver.find_element(
#     By.XPATH, "//p[contains(text(), 'Batting & Fielding')]/following-sibling::div/table"
# )
# batting_fielding_stats = extract_t20_stats(batting_fielding_table)

# # Locate the bowling stats table and extract T20 stats
# bowling_table = driver.find_element(
#     By.XPATH, "//p[contains(text(), 'Bowling')]/following-sibling::div/table"
# )
# bowling_stats = extract_t20_stats(bowling_table)

# # Close the WebDriver
# driver.quit()

# # Combine batting and bowling stats
# combined_stats = batting_fielding_stats + bowling_stats

# import os

# # File path for the CSV
# csv_file_path = "t20_combined_stats.csv"

# # Check if the file exists and is empty
# file_exists = os.path.isfile(csv_file_path)
# file_empty = os.stat(csv_file_path).st_size == 0 if file_exists else True

# # Open the file in append mode
# with open(csv_file_path, "a", newline="") as file:
#     writer = csv.writer(file)
#     # Write the player's stats
#     writer.writerow(combined_stats)


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time, csv, os


# Function to extract T20 stats from a given table
def extract_t20_stats(table):
    rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
    for row in rows:
        first_cell_text = row.find_element(By.CSS_SELECTOR, "td").text
        if "T20s" in first_cell_text:
            return [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
    return []


# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--ignore-ssl-errors=yes")
chrome_options.add_argument("--ignore-certificate-errors")

# File path for the CSV
csv_file_path = "old_t20_combined_stats.csv"

# Read player names from the CSV file
with open("oldplayers.csv", "r", encoding="utf-8-sig") as file:
    reader = csv.reader(file)
    player_names = [
        row[0] for row in reader
    ]  # Adjust depending on the structure of your CSV

for player_name in player_names:
    try:
        driver = webdriver.Chrome(options=chrome_options)

        # Navigate to the webpage
        driver.get("https://search.espncricinfo.com/ci/content/site/search.html")
        time.sleep(3)  # Wait for the page to load

        search_input = driver.find_element(
            By.XPATH, '//*[@id="primary-search"]/div/div/input[1]'
        )
        search_input.send_keys(player_name)  # Use player name from the list
        search_input.send_keys(Keys.ENTER)
        time.sleep(3)  # Wait for search results to load

        # search_result = driver.find_element(
        #     By.XPATH, '//*[@id="viewport"]/div[5]/div[2]/main/div/div[4]/ul/li'
        # )
        # link = search_result.find_element(By.TAG_NAME, "a").get_attribute("href")
        # driver.get(link)

        # time.sleep(3)  # Wait for player page to load
        combined_stats = []
        try:
            search_result = driver.find_element(
                By.XPATH, '//*[@id="viewport"]/div[5]/div[2]/main/div/div[4]/ul/li'
            )
            link = search_result.find_element(By.TAG_NAME, "a").get_attribute("href")
            driver.get(link)
            time.sleep(5)
            # Extract stats
            batting_fielding_table = driver.find_element(
                By.XPATH,
                "//p[contains(text(), 'Batting & Fielding')]/following-sibling::div/table",
            )
            batting_fielding_stats = extract_t20_stats(batting_fielding_table)
            bowling_table = driver.find_element(
                By.XPATH,
                "//p[contains(text(), 'Bowling')]/following-sibling::div/table",
            )
            bowling_stats = extract_t20_stats(bowling_table)
            combined_stats = batting_fielding_stats + bowling_stats

            # Check if the file exists and is empty
            file_exists = os.path.isfile(csv_file_path)
            file_empty = os.stat(csv_file_path).st_size == 0 if file_exists else True

            # Append player stats to CSV
            with open(csv_file_path, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([player_name] + combined_stats)

        except NoSuchElementException:
            print(f"No search results found for player: {player_name}")
            # Check if the file exists and is empty
            file_exists = os.path.isfile(csv_file_path)
            file_empty = os.stat(csv_file_path).st_size == 0 if file_exists else True

            # Append player stats to CSV
            with open(csv_file_path, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([player_name])
            continue  # Skip to the next player

    finally:
        driver.quit()

    # # Check if the file exists and is empty
    # file_exists = os.path.isfile(csv_file_path)
    # file_empty = os.stat(csv_file_path).st_size == 0 if file_exists else True

    # # Append player stats to CSV
    # with open(csv_file_path, "a", newline="") as file:
    #     writer = csv.writer(file)
    #     writer.writerow([player_name] + combined_stats)
