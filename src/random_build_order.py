import json
import random
from os import listdir

from src.url import list_all_builds_order
from src.manage import BUILD_DB_NAME, BUILD_DB_PATH
from src.build_order import BuildOrder

class RandomBuildOrder(BuildOrder):
    """Create a random build order randomly choosen among all defined"""

    def __init__(self):
        # Look for the list of all build order stored
        # If the json file isn't created, make it
        if BUILD_DB_NAME not in listdir("src"):
            list_all_builds_order()

        # Open the json file
        with open(BUILD_DB_PATH, "r") as fp:
            builds = json.load(fp)

        # Retrieve all the index found
        index_bo_list = [int(k) for k in builds.keys()]

        # Randomize the build order choice
        build_index = random.randint(min(index_bo_list), max(index_bo_list))
        href = builds[str(build_index)]

        # Create a BuildOrder object with the random link
        super().__init__(href)
