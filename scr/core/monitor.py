from scraper.universal import get_price
from database.db import get_all_products, save_price

def check_all_products():
    products = get_all_products()

    for product in products:
        print(f"Checking: {product['name']}")

        price = get_price(product["url"], product["selector"])
        print(f"Price: {price}")

        save_price(product["id"], price)
