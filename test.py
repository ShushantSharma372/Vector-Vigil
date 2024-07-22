
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service('/usr/local/bin/chromedriver')
    global driver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    username = input("Enter Instagram username: ")
    password = input("Enter Instagram password: ")
    log_insta(username, driver, password)
    input("Press Enter to close.")  # Hold the script open
    driver.quit()

def log_insta(username, driver, password):
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(3)  # Allow time for the page to load
    username_input = driver.find_element(By.NAME, 'username')
    password_input = driver.find_element(By.NAME, 'password')
    username_input.send_keys(username)
    password_input.send_keys(password)
    login_button = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')  
    login_button.click()
    time.sleep(8)  # Allow time for login to process

if __name__ == "__main__":
    main()
