from scraper.universal import get_price
from database.db import get_all_products, save_price
from notifier.telegram import send_telegram

def check_all_products():
    products = get_all_products()

    if not products:
        print("No products. Add via menu option 1.")
        return

    for product in products:
        name   = product["name"]
        target = product["target_price"]
        url    = product["url"]

        print(f"\n🔍 Checking: {name}")

        price = get_price(url, product["selector"])

        if price is None:
            print(f"   ⚠️  Failed to get price")
        else:
            print(f"   💰 Price: {price}")

            if price <= target:
                print(f"   🎯 PRICE REACHED TARGET! ({price} <= {target})")

                text = (
                    f"🎯 PriceWatcher: price reached target!\n\n"
                    f"Product: {name}\n"
                    f"Current price: {price}\n"
                    f"Your target: {target}\n"
                    f"Link: {url}"
                )

                print("   Sending notification...")
                send_telegram(text)

            else:
                print(f"    Still not reached target {target}")

        save_price(product["id"], price)
