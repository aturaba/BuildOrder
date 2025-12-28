
import json
from typing import Any
from os import listdir, mkdir
from inspect import currentframe
from src.manage import MAIN_URL, BUILD_DB_PATH

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.firefox import GeckoDriverManager

MAX_TIMEOUT_IN_WAIT = 1

def _timeout_func(func_name:str):
    """Message Generator for TimeoutException in selenium 'until' method"""
    return f"TimeoutException Raised in '{func_name}' after {MAX_TIMEOUT_IN_WAIT}s"

def get_url(url:str, div_root:str) -> list[WebElement]:
    """
    Create a driver used to parse the HTML page.
    Return the selected root element.
    Using Selenium to handle the page update, for non static elements

    Args:
        url (str): url of the website
        div_root (str): CSS class name of the root to use

    Returns:
        list[WebElement]: list of the WebElement found in the page
    """

    # Define the driver option and create it
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(
        service=Service(GeckoDriverManager().install()),
        options=options
    )
    driver.get(url)

    # Wait the website to update, get the requested root
    wait = WebDriverWait(driver, 1)
    root = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, div_root)),
        _timeout_func(currentframe().f_code.co_name),
    )

    return root

def parse_root_without_condition(root:list[WebElement], *tup_def:tuple[str]) -> list[WebElement]:
    """
    Parse recursively inside a list of several CSS class definition.
    Use the firs element found of each step

    Args:
        root (list[WebElement]): First element to dig into
        tup_def (tuple[str]): all CSS class to look for, one by one

    Returns:
        list[WebElement]: elements found after the parsing
    """

    # Get the first element of the parsing list
    current_root = root[0]

    for class_name_type in tup_def:
        # For each depth, update the root to use
        current_root = current_root.find_elements(
            By.CSS_SELECTOR,
            class_name_type
        )[0]

    return current_root

def list_all_builds_order():
    """
    List all build orders found in the homepage, save their url into a json file.
    "Static" folder is created if it isn't already.
    """

    # Get the root of the homepage
    url = MAIN_URL
    root = get_url(url, "div[id*='root']")

    # List all the panels found
    div_all_builds = root[0].find_elements(
        By.CSS_SELECTOR,
        "div[class*='w-11/12 md:w-10/12 lg:w-9/12 mx-auto mb-10 flex flex-wrap justify-center']"
    )

    # Wait for the update 
    # TODO : why do we need to wait again ? get_url is already done
    builds = WebDriverWait(div_all_builds[0], MAX_TIMEOUT_IN_WAIT).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "a")),
        _timeout_func(currentframe().f_code.co_name),
    )

    # Retrieve the link of the build order, save it into a dictionnary
    build_dict_export = {
        k : elt.get_attribute("href")
        for k, elt in enumerate(builds)
    }

    # Verify if the static folder is already created
    if "static" not in listdir():
        mkdir("static")
    
    # Export the dictionnay into a json file
    export_json(build_dict_export, BUILD_DB_PATH)

def export_json(data:dict[Any, Any], filename:str):
    """
    Export a selected dictionnary into a json file.
    File extension isn't checked, .json is mandatory in 'filename' definition

    Args:
        data (dict[Any, Any]): current dictionnary to export
        filename (str): filepath to the json file
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
