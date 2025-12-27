
import json
from os import listdir, mkdir
from src.manage import MAIN_URL, BUILD_DB_PATH
from typing import Any

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

def list_all_builds_order():
    url = MAIN_URL
    root = get_url(url, "div[id*='root']")

    div_all_builds = root[0].find_elements(
        By.CSS_SELECTOR,
        "div[class*='w-11/12 md:w-10/12 lg:w-9/12 mx-auto mb-10 flex flex-wrap justify-center']"
    )

    builds = WebDriverWait(div_all_builds[0], 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
    )

    build_dict_export = {
        k : elt.get_attribute("href")
        for k, elt in enumerate(builds)
    }

    if "static" not in listdir():
        mkdir("static")
    
    export_json(build_dict_export, BUILD_DB_PATH)

def export_json(data:dict[Any, Any], filename:str):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
