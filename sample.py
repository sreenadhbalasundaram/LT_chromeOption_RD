from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from time import sleep
import os
import base64

# Chrome options for media stream testing
chrome_options = ChromeOptions()
chrome_options.add_argument("--use-fake-ui-for-media-stream")  # Auto-allow permissions
chrome_options.add_argument("--use-fake-device-for-media-stream")  # Simulate mic input
chrome_options.add_argument("--allow-file-access-from-files")
chrome_options.add_argument("--allow-file-access")
chrome_options.add_argument("--disable-infobars")  # Hide permission popups
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-popup-blocking")  # Ensure popups don’t interfere

# Load Appium capabilities and merge Chrome options
capabilities = UiAutomator2Options().load_capabilities({
    "lt:options": {
        "browserName": "Chrome",
        "w3c": True,
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "deviceName": "Galaxy.*",
        "platformVersion": "12",
        "isRealMobile": True,
        "build": "Push validation",
        "name": "Push Validation",
        "visual": True,
        "network": True,
        "console": True,
        "goog:chromeOptions": {
            "args": chrome_options.arguments  # Injecting Chrome options
        }
    }
})

def starting_test():
    # Set username and access key from environment variables or default values
    username = os.getenv("LT_USERNAME", "sreenadhb")
    access_key = os.getenv("LT_ACCESS_KEY", "I304plaCpBxpERvH5roJ6vFuWqLf4lokSJv2Bb1JvgIF0pjqbH")

    driver = None
    try:
        # Initiate a remote WebDriver session with the corrected options reference
        driver = webdriver.Remote(
            f"https://{username}:{access_key}@mobile-hub.lambdatest.com/wd/hub",
            options=capabilities
        )
        
        wait = WebDriverWait(driver, 30)
        print("Session ID:", driver.session_id)

        # Navigate to a sample app page
        driver.get("https://mictests.com/check")
        
        sleep(20)

        # Wait for and click the "Test My Mic" button
        test_my_mic = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='mic-launcher']"))
        )
        test_my_mic.click()
    
        # Path to the file on your local system
        local_file_path = "C:/Users/sreenadhb/Downloads/image (29).png"   #filepath in local 

        # Read the file in binary mode and encode it to Base64
        with open(local_file_path, "rb") as file:
            file_data = base64.b64encode(file.read()).decode("utf-8")

        # Destination path on the device
        dest_path = "/sdcard/Downloads/sampleimage.png"    # filename in RD

        # Push the file to the device
        driver.push_file(dest_path, file_data)

        # Pull the file back to verify
        file_base64 = driver.pull_file(dest_path)

        # Decode and save the pulled file (Optional: For verification)
        pulled_file_path = "C:/Users/sreenadhb/Python mobile browser/sample.png"
        with open(pulled_file_path, "wb") as file:
            file.write(base64.b64decode(file_base64))

        print(f"File successfully pushed to {dest_path} and pulled back to {pulled_file_path}")

        # Allow the test to run for 150 seconds
        sleep(150)
    
    except Exception as e:
        print(f"Error: {str(e)}")
    
    finally:
        # Ensure the driver quits properly even if an error occurs
        if driver:
            driver.quit()

starting_test()

