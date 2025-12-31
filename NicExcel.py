
import json
import time
from datetime import datetime, timedelta
import multiprocessing as mp
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



if __name__ == '__main__':
    mp.freeze_support()
    with open('config.json', 'r', encoding="utf-8") as file:
        config = json.load(file)
    start_time_ = time.strftime("%H-%M-%S")
    current_date = datetime.now().strftime("%Y%m%d-%H:%M")
    previous_date = datetime.now() - timedelta(days=1)
    previous_date = previous_date.strftime("%Y%m%d")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
