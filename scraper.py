from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time

# Set the path to your Geckodriver executable
geckodriver_path = "geckodriver.exe"

# Configure Firefox options
firefox_options = FirefoxOptions()

# Disable automation flags
firefox_options.set_preference("dom.webdriver.enabled", False)  # Disable WebDriver flag
firefox_options.set_preference("useAutomationExtension", False)  # Disable automation extension

# Set a custom user agent
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
firefox_options.set_preference("general.useragent.override", user_agent)

# Disable various features that can reveal automation
firefox_options.set_preference("webgl.disabled", True)  # Disable WebGL
firefox_options.set_preference("media.peerconnection.enabled", False)  # Disable WebRTC
# firefox_options.set_preference("permissions.default.image", 2)  # Disable images
firefox_options.set_preference("javascript.enabled", True)  # Ensure JavaScript is enabled

# Initialize the Firefox WebDriver using FirefoxService and FirefoxOptions
service = FirefoxService(executable_path=geckodriver_path)
driver = webdriver.Firefox(service=service, options=firefox_options)

try:
    # Open Google
    driver.get("https://www.google.com")

    # Find the search box element by name
    search_box = driver.find_element(By.NAME, "q")

    # Type a search query
    search_box.send_keys("Python Selenium Geckodriver")

    # Press Enter to perform the search
    search_box.send_keys(Keys.RETURN)

    # Wait for the results to load
    time.sleep(3)

    # Print the title of the page
    print("Page title:", driver.title)

finally:
    # Close the browser
    driver.quit()