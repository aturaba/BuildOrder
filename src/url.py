
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager

def get_url(url:str, div_root:str):
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(
        service=Service(GeckoDriverManager().install()),
        options=options
    )

    driver.get(url)
    wait = WebDriverWait(driver, 1)
    root = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, div_root)))

    return root

def parse_root_without_condition(root, *tup_def):
    current_root = root[0]
    for class_name_type in tup_def:
        current_root = current_root.find_elements(
        By.CSS_SELECTOR,
        class_name_type
    )[0]

    return current_root