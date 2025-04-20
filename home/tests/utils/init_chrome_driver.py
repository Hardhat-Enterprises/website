"""
@author: CHUNYI WANG
@file: init_chrome_driver
@time: 2025/4/9 14:17
@desc: Initialize a chromium driver to post data to urls
"""

import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def init_driver():
    # kill exists processess
    os.system("pkill -f chrome")
    os.system("pkill -f chromedriver")
    time.sleep(1)

    # Configure chromium driver
    options = webdriver.ChromeOptions()
    # options.binary_location = "/usr/bin/chromium-browser"
    options.add_argument("--user-data-dir=/tmp/chrome-test-profile")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new") 
    options.add_argument("--enable-logging")
    options.add_argument("--v=1")
    
    # init the driver
    try:
        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
    except Exception as e:
        print(f"Driver initialization failure: {str(e)}")
        raise