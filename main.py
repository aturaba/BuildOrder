from src.build_order import BuildOrder
from src.random_build_order import RandomBuildOrder

# Load a Build Order randomly choosen
RandomBuildOrder()

# Load a Build Order choosen by the user
url = "https://buildorderguide.com/#/build/4wh2hU9oXBfK3oUzbeez"
BuildOrder(url)
