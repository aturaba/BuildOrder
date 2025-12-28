"""BuildOrder Class Definition"""

from typing import Union
from src.url import get_url, parse_root_without_condition, export_json
from selenium.webdriver.common.by import By

class BuildOrder:
    """Create a random build order with the selected url"""

    url: str
    name: str
    ressources_list: list[str]
    step_list: list[str]
    step_dict: dict[Union[str, int], str]

    def __init__(self, url:str):
        self.url = url

        self.step_list : list[str] = []
        self.step_dict : dict[Union[str, int], str] = {"url" : url}

        self._root = get_url(url, "div[class*='flex flex-col space-y-4']")

        self.name = self._get_header()
        self.ressources_list = self._get_ressources_list()

        # Read the build order steps, and save it
        self._get_order_list()

        # Export the build order
        for i, value in enumerate(self.step_list):
            self.step_dict[i] = value

        export_json(self.step_dict, "build_order.json")

        print(f"\033[34m{self.name}\033[0m")
        print(f"\033[34m{self.url}\033[0m")
        print(f"\033[34mbuild_order.json created\033[0m")

    def _get_header(self):
        civ_type = parse_root_without_condition(
            self._root,
            "div[class*='flex justify-center mt-10 -mb-10']",
            "div[class*='flex space-x-1 text-main-dark']",
            "span[class*='pt-1']"
        ).text

        build_order_name = parse_root_without_condition(
            self._root,
            "div[class*='text-center']",
            "h1[class*='text-primary-dark my-10 uppercase font-bold tracking-widest text-2xl text-center']",
        ).text

        self.step_dict["civ_name"] = civ_type
        self.step_dict["build_order_name"] = build_order_name

        return build_order_name

    def _get_ressources_list(self):

        ressources_div = parse_root_without_condition(
            self._root,
            "div[class*='flex flex-col w-11/12 md:max-w-2xl m-auto text-main-dark pb-16 text-xs md:text-base']",
            "div[class*='flex justify-end']",
            "div[class*='w-full grid overflow-hidden grid-cols-12 grid-rows-1']",
            "div[class*='col-start-10 md:col-start-9 col-span-3 md:col-span-4 flex justify-around w-full']",
        )

        ressources_list = [
            div.get_attribute("Alt")
            for div in ressources_div.find_elements(By.CSS_SELECTOR, "img[class*='w-4 h-4 md:w-6 md:h-6']")
        ]

        return ressources_list


    def _get_one_line_grid(self, grid_line):
        # List the action to realize
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

            # For each ressources, show the villager count to consider
            ressources_str_list = [
                f"{self.ressources_list[k]} : {ressources_elt.text}"
                for k, ressources_elt in enumerate(ressources_grid_p)
            ]
            step_text += " | ".join(ressources_str_list)

        return step_text

    def _get_order_list(self):
        steps = self._root[0].find_elements(
            By.CSS_SELECTOR,
            "div[class*='flex flex-col w-11/12 md:max-w-2xl m-auto text-main-dark pb-16 text-xs md:text-base']"
        )
        # Initialize the actions step list
        self.step_list.append("======= Dark Age =======")
        for parent in steps:
            children = parent.find_elements(By.CSS_SELECTOR, "*")

            # Depending on the class type, return a specific text
            for child in children:
                step_text = ""

                # Build Order step, containing actions and current villager count
                if child.get_attribute("class") == "grid overflow-hidden grid-cols-12 grid-rows-1":
                    step_text += self._get_one_line_grid(child)

                # Action to realize during Age transition
                elif child.get_attribute("class") == "italic my-4 text-xl":
                    step_text += f"   ==== {child.text} ==="

                # Current Age
                elif child.get_attribute("class") == "flex my-4 text-xl":
                    step_text += f"======= {child.text} ======"

                # Append the actions
                if step_text != "":
                    self.step_list.append(step_text)
