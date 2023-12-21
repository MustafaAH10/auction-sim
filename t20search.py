from selenium import webdriver
import time
import csv

# List of player names
players = [
    "harry brook",
    "travis head",
    "Rilee Rossouw",
]  # Replace with your list of 300 players

# Set up Selenium WebDriver
driver = webdriver.Chrome()  # Replace with your WebDriver


# Function to search and extract T20 stats
def get_t20_stats(player_name):
    search_query = f"{player_name} stats"
    driver.get(f"https://www.google.com/search?q={search_query}")
    time.sleep(2)  # Wait for page to load
    try:
        # Find the table row containing T20 stats - this XPath is hypothetical
        stats_row = driver.find_element_by_xpath(
            '//*[@id="kp-wp-tab-default_tab:kc:/sports/pro_athlete:stats"]/div[1]/div/div/div[2]/div/div/div/stats-table[1]/div/table/tbody/tr[7]'
        )
        print(stats_row)
        print(stats_row.text)
        return stats_row.text
    except:
        return "Stats not found"


# Open file to write stats
with open("player_stats.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Player", "T20 Stats"])

    # Iterate over each player and write their stats to the file
    for player in players:
        stats = get_t20_stats(player)
        writer.writerow([player, stats])
        time.sleep(1)  # Delay to prevent rapid-fire requests

# Close the WebDriver
driver.quit()
