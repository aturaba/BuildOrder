import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from src.url import get_url, parse_root_without_condition
from selenium.webdriver.support import expected_conditions as EC
from src.build_order import BuildOrder

class RandomBuildOrder(BuildOrder):

    def __init__(self):
        self.url = "https://buildorderguide.com"

        self.root = get_url(self.url, "div[id*='root']")

        self.div_all_builds = self.root[0].find_elements(
            By.CSS_SELECTOR,
            "div[class*='w-11/12 md:w-10/12 lg:w-9/12 mx-auto mb-10 flex flex-wrap justify-center']"
        )

        builds = WebDriverWait(self.div_all_builds[0], 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
        )

        build_index = random.randint(0, len(builds))
        href = builds[build_index].get_attribute("href")

        super().__init__(href)