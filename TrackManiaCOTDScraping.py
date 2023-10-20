from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.firefox.options import Options


import pandas as pd
import tqdm


# Converts time in string to seconds
def convert_to_seconds(time_str):
    minutes, seconds = time_str.split(":")
    seconds, milliseconds = seconds.split(".")
    return int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000.0


def scrap_COTD(ID):
    # Creates a mozilla firefox driver with geckodriver
    # You need to install geckdriver.exe (https://github.com/mozilla/geckodriver/releases)

    # Then you installation path (geckdriver.exe location)
    GECKDRIVER_PATH = "C:/Users/jimit/OneDrive/Documents/2. INFORMATIQUE/Python/selenium-test/geckodriver.exe"

    # Creates the driver
    service = Service(GECKDRIVER_PATH)
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(service=service, options=options)

    sleep(0.5)

    # Opens TM.IO at the right COTD page
    driver.get('https://trackmania.io/#/cotd/' + str(ID))

    # Page loading
    sleep(1)

    # Button to load more players
    button = driver.find_elements(By.CLASS_NAME, "button.is-fullwidth.is-info")[-1]

    # Finding the number of players 
    body = driver.find_elements(By.CSS_SELECTOR, "tbody")[0]
    player_row = driver.find_elements(By.CSS_SELECTOR, "tr")[0]
    player_number = driver.find_elements(By.CSS_SELECTOR, "td")[0]
    player_amout = int(player_number.text)

    # Calculating how many times we have to press on "more players"
    k = int((player_amout) / 15)

    # Scrolling the page and pressing "more players" button
    for i in tqdm.tqdm(range(k)):
        sleep(0.2)
        button = driver.find_elements(By.CLASS_NAME, "button.is-fullwidth.is-info")[-1]
        button.click()
        sleep(0.55)
        actions = ActionChains(driver)
        for i in range(3):
            button = driver.find_elements(By.CLASS_NAME, "button.is-fullwidth.is-info")[-1]
            try:
                button.send_keys(Keys.PAGE_DOWN)
                break  
            except StaleElementReferenceException:
                print(f"Essai {i+1} échoué. Retenter...")

    # Finds all the right side rows
    rows = driver.find_elements(By.XPATH, "//tr[@data-v-66c3cac2]")

    # Ranking starts at row n°6
    rows = rows[5:]

    print(len(rows), " players has been scraped")


    ranks = []
    players = []
    times_str = []

    # Parses all the rows and retrieves the data
    for i in rows:
        ranks.append(i.find_elements(By.CSS_SELECTOR, 'td')[0].text)

        players.append(i.find_elements(By.CSS_SELECTOR, 'td')[1].text)

        time = i.find_elements(By.CSS_SELECTOR, 'td')[2]
        times_str.append(time.find_element(By.CSS_SELECTOR, 'span').text)

    # Closes the driver
    driver.close()


    times = [convert_to_seconds(i) for i in times_str]

    # Saves the data on a dataframe
    dic = {"rank":ranks,
        "player":players,
        "time":times}

    df = pd.DataFrame(dic)

    # returns the dataframe
    return(df)