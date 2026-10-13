import requests
from bs4 import BeautifulSoup

def get_price(url, selector):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    tag = soup.select_one(selector)
    if not tag:
        print("Element not found for selector:", selector)
        return None

    text = tag.text.strip()

    cleaned = (
        text.replace("€", "")
            .replace("$", "")
            .replace(",", ".")
            .strip()
    )

    try:
        return float(cleaned)
    except:
        print("Failed to convert price:", text)
        return None
