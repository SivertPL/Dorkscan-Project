import requests
import urllib 

from urllib.parse import urlparse, parse_qsl

HEURISTIC_CHECK_ALPHABET = ('"', '\'', ')', '(', ',', '.')


def sort_urls(urls):
    tmp_duplicate_list = []
    sorted_urls = []
    for url in urls:
        if is_garbage(url):
            continue
        host = url.split("/", 3)
        domain = host[2]
        if domain not in tmp_duplicate_list and "=" in url:
            tmp_duplicate_list.append(domain)
            sorted_urls.append(url)

    return sorted_urls

def u_round(x, base=5):
    return int(base * round(float(x)/base))

def fire_and_forget(url):
    try:
        response = requests.get(url, timeout=2)
        response.raise_for_status()
    except Exception:
        return ''
    return response.text

def progressbar(fill_amount, max_amount):
    percent = 1.0 * fill_amount / max_amount * 100
    amount = int(10 * (percent / 100))
    bar = "[" + ("#" * amount) + ("-" * (10 - amount)) + "]"
    return bar


def is_garbage(url):
    parsed = urlparse(url)

    params = parse_qsl(parsed.query)

    if len(params) == 0 or "blogspot.com" in url:
        return True
