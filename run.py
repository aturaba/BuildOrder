from pprint import pprint
from src.build_order import BuildOrder

DIV_CONTAINER = {
    "civ" : "div[class*='flex space-x-1 text-main-dark']",
    "difficulty" : "div[class*='flex bg-secondary-light pl-1 pr-2 rounded-md']",
}

container = "civ"

bo = BuildOrder("https://buildorderguide.com/#/build/n82S5EBP0X4bNt4flILo")
pprint(bo.step_list)
