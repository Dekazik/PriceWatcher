import time

from database.db import add_product, init_db, get_all_products, delete_product
from core.monitor import check_all_products
from pathlib import Path

CONFIG_FILE = Path(__file__).resolve().parent / "core" / "config.py"


def show_menu():
    print("\n" + "="*40)
    print("       💰 PriceWatcher")
    print("="*40)
    print("  1 — Add product")
    print("  2 — Check prices now")
    print("  3 — Show all products")
    print("  4 — Show price history")
    print("  5 — Delete product")
    print("  6 — Notification settings")
    print("  7 — Auto-monitor settings")
    print("  0 — Exit")
    print("="*40)

def auto_monitor_menu():
    print("\n--- Auto-monitor settings ---")

    try:
        while True:
            check_all_products()
            print("Next check in 30 minutes. Press Ctrl+C to stop.")
            time.sleep(30)

    except KeyboardInterrupt:
        print("\nStopping auto-monitor.")


def add_product_menu():
    print("\n--- Add product ---")
    name     = input("Product name: ").strip()
    url      = input("Product URL: ").strip()
    selector = input("Price CSS selector: ").strip()
    target   = input("Target price (when to notify): ").strip()

    try:
        target = float(target.replace(",", "."))
    except ValueError:
        print("❌ Invalid price. Enter a number, e.g., 99.99")
        return

    add_product(name, url, selector, target)
    print(f"✅ Product '{name}' added!")

def show_products_menu():
    products = get_all_products()
    if not products:
        print("\nNo products to display. Add a product using option 1.")
        return

    print("\n--- All products ---")
    for p in products:
        print(f"  [{p['id']}] {p['name']}")
        print(f"       URL: {p['url']}")
        print(f"       Target price: {p['target_price']}")
        print()

def show_history_menu():
    from database.db import get_price_history
    products = get_all_products()
    if not products:
        print("\nNo products to display. Add a product using option 1.")
        return

    print("\n--- Price history ---")
    for p in products:
        history = get_price_history(p["id"])
        print(f"\n📦 {p['name']} (target: {p['target_price']})")
        if not history:
            print("   No history available. Run a check (option 2).")
        else:
            for row in history[-5:]:
                price, ts = row
                mark = "🎯" if price is not None and price <= p["target_price"] else "  "
                price_str = f"{price}" if price is not None else "failed to retrieve"
                print(f"   {mark} {price_str}  [{ts}]")

def delete_product_menu():
    products = get_all_products()
    if not products:
        print("\nNo products to delete.")
        return

    print("\n--- Delete product ---")
    for p in products:
        print(f"  [{p['id']}] {p['name']}")

    choice = input("\nEnter the ID of the product to delete (or press Enter to cancel): ").strip()
    if not choice:
        print("Cancellation.")
        return

    try:
        pid = int(choice)
    except ValueError:
        print("❌ Invalid ID.")
        return

    ids = [p["id"] for p in products]
    if pid not in ids:
        print("❌ Product with such ID not found.")
        return

    delete_product(pid)
    print(f"✅ Product deleted.")

def settings_menu():
    import core.config as cfg

    print("\n--- Notification settings ---")
    print("Current values:")
    print(f"  Telegram token:   {'✅ filled' if cfg.TELEGRAM_TOKEN else '❌ empty'}")
    print(f"  Telegram chat ID: {'✅ filled' if cfg.TELEGRAM_CHAT_ID else '❌ empty'}")
    print()
    print("What to configure?")
    print("  1 — Telegram")
    print("  2 — Check (send test)")
    print("  0 — Back")

    choice = input("Choice: ").strip()

    if choice == "1":
        token   = input("Telegram token (Enter — leave as is): ").strip()
        chat_id = input("Telegram Chat ID (Enter — leave as is): ").strip()
        _save_config(
            telegram_token   = token   or cfg.TELEGRAM_TOKEN,
            telegram_chat_id = chat_id or cfg.TELEGRAM_CHAT_ID,
        )
        print("✅ Saved! Restart the program to apply changes.")

    elif choice == "2":
        print("\nSending test message...")
        from notifier.telegram import send_telegram
        send_telegram("✅ PriceWatcher: test Telegram works!")

    else:
        print("Back.")


def _save_config(telegram_token, telegram_chat_id):
    content = f'''
TELEGRAM_TOKEN   = "{telegram_token}"
TELEGRAM_CHAT_ID = "{telegram_chat_id}"
'''
    CONFIG_FILE.write_text(content, encoding="utf-8")


def cli():
    init_db()
    while True:
        show_menu()
        choice = input("Choice: ").strip()

        if choice == "1":
            add_product_menu()
        elif choice == "2":
            print("\n--- Checking prices... ---")
            check_all_products()
        elif choice == "3":
            show_products_menu()
        elif choice == "4":
            show_history_menu()
        elif choice == "5":
            delete_product_menu()
        elif choice == "6":
            settings_menu()
        elif choice == "7":
                auto_monitor_menu()
        elif choice == "0":
            print("Goodbye! 👋")
            break
        else:
            print("❌ Invalid choice, please try again.")

if __name__ == "__main__":
    cli()
