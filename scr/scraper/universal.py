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
        .replace("£", "")
        .replace("Â", "")
        .replace(" ", "")
        .strip()
)

    if "," in cleaned and "." in cleaned:
        if cleaned.rfind(",") > cleaned.rfind("."):
            cleaned = cleaned.replace(".", "").replace(",", ".")
        else:
            cleaned = cleaned.replace(",", "")
    elif "," in cleaned:
        cleaned = cleaned.replace(",", ".")

    try:
        return float(cleaned)
    except:
        print("Failed to convert price:", text)
        return None
