from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from datetime import date
import os
import json

CHROME_DRIVE_PATH = os.path.join(os.getcwd(), "chromedriver")
OP = webdriver.ChromeOptions()
OP.add_argument('--headless')
DRIVER = webdriver.Chrome(CHROME_DRIVE_PATH)


def login():
    with open('config.json') as configFile:
        credentials = json.load(configFile)
        time.sleep(2)
        DRIVER.find_element(By.XPATH, value="//a[@href='/login']").click()
        time.sleep(2)
        username = DRIVER.find_element(
            By.CSS_SELECTOR, value="input[name='user']")
        username.clear()
        username.send_keys(credentials["USERNAME"])
        time.sleep(2)
        DRIVER.find_element(By.CSS_SELECTOR, value=(
            "input[type='submit']")).click()
        time.sleep(2)
        password = DRIVER.find_element(
            By.CSS_SELECTOR, value="input[name='password']")
        password.clear()
        password.send_keys(credentials["PASSWORD"])
        DRIVER.find_element(By.ID, value="login-submit").click()
        time.sleep(5)


def main():
    try:
        DRIVER.get("https://trello.com")
        login()
        input("Bot Operation Completed. Press any key...")
        DRIVER.close()
    except Exception as e:
        print(e)
        DRIVER.close()


if __name__ == "__main__":
    main()
