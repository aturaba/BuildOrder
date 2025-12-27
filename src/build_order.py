"""BuildOr"""
import os
os.environ["GH_TOKEN"] = "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"

import json
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager

class BuildOrder:

    def __init__(self, url:str):
        self.url = url
        self.wait = self._get_url()

        self.step_list : list[str] = []
        self._get_action_list()

    def _get_url(self):
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(
            service=Service(GeckoDriverManager().install()),
            options=options
        )

        driver.get(self.url)
        wait = WebDriverWait(driver, 1)

        return wait

    def _get_one_line_grid(self, grid_line):
        # List the action to realize
        ressources_list = ["wood", "food", "gold", "stone"]
        step_text = ""

        # List the action to realize
        action = "div[class*='box row-start-1 row-end-auto col-span-9 md:col-span-8']"
        action_div = grid_line.find_elements(By.CSS_SELECTOR, action)
        if len(action_div) > 0:
            step_text += action_div[0].text

        # Ressources Villagers Count
        villager_div = grid_line.find_elements(By.CSS_SELECTOR, "div[class*='box col-span-3 md:col-span-4']")
        if len(villager_div) > 0:
            step_text += " → "
            ressources_grid_div = villager_div[0].find_elements(By.CSS_SELECTOR, "div[class*='flex justify-around w-full']")
            ressources_grid_p = ressources_grid_div[0].find_elements(By.CSS_SELECTOR, "p[class*='w-4 h-4 md:w-6 md:h-6 text-center']")

            ressources_str_list = [
                f"{ressources_list[k]} : {ressources_elt.text}"
                for k, ressources_elt in enumerate(ressources_grid_p)
            ]
            step_text += " | ".join(ressources_str_list)

        return step_text

    def _get_action_list(self):
        steps = self.wait.until(
            EC.presence_of_all_elements_located(
                (
                    By.CSS_SELECTOR,
                    "div[class*='flex flex-col w-11/12 md:max-w-2xl m-auto text-main-dark pb-16 text-xs md:text-base']"
                )
            )
        )

        self.step_list.append("======= Dark Age =======")
        for parent in steps:

            children = parent.find_elements(By.CSS_SELECTOR, "*")

            for child in children:
                step_text = ""

                if child.get_attribute("class") == "grid overflow-hidden grid-cols-12 grid-rows-1":
                    step_text += self._get_one_line_grid(child)

                elif child.get_attribute("class") == "italic my-4 text-xl":
                    step_text += f"   ==== {child.text} ==="

                elif child.get_attribute("class") == "flex my-4 text-xl":
                    step_text += f"======= {child.text} ======"

                if step_text != "":
                    self.step_list.append(step_text)

        step_dict = {i: value for i, value in enumerate(self.step_list)}

        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(step_dict, f, indent=4, ensure_ascii=False)
