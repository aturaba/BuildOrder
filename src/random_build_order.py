from os import listdir
import random
import json
from src.manage import BUILD_DB_NAME, BUILD_DB_PATH
from src.url import list_all_builds_order
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from src.build_order import BuildOrder

class RandomBuildOrder(BuildOrder):

    def __init__(self):

        if BUILD_DB_NAME not in listdir("src"):
            list_all_builds_order()

        with open(BUILD_DB_PATH, "r") as fp:
            builds = json.load(fp)

        index_bo_list = [int(k) for k in builds.keys()]

        build_index = random.randint(min(index_bo_list), max(index_bo_list))
        href = builds[str(build_index)]

        super().__init__(href)
