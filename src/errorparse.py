import urllib
import xml.dom.minidom 
import urllib.parse as urlparse
import xml.etree.ElementTree
import re 

from urllib.parse import urlencode, unquote, urlparse, parse_qs, ParseResult, parse_qsl
from xml.dom import minidom 
from util import HEURISTIC_CHECK_ALPHABET
from random import choice

regexp_loaded = []
regexp_cache = {}

def parse_errors_file():
    xmldoc = minidom.parse('lists/errors.xml')
    list = xmldoc.getElementsByTagName('error')
    for item in list:
        error = item.attributes['regexp'].value
        regexp_loaded.append(error)
    print("Loaded {}".format(len(regexp_loaded)))

def check_error_present(response):
    for regexp in regexp_loaded:
        if regexp not in regexp_cache:
            keywords = re.findall(r"\w+", re.sub(r"\\.", " ", regexp))
            keywords = sorted(keywords, key=len)
            regexp_cache[regexp] = keywords[-1].lower()
        if regexp_cache[regexp] in response.lower() and re.search(regexp, urllib.parse.unquote(response), re.I):
            return regexp
    if re.search(r"SQL (warning|error|syntax)", response, re.I):
        return "generic"

def add_url_params(url, params):
    url = unquote(url)
    parsed_url = urlparse(url)
    get_args = parsed_url.query
    parsed_get_args = dict(parse_qsl(get_args))
    parsed_get_args.update(params)

    encoded_get_args = urlencode(parsed_get_args, doseq=True)

    new_url = ParseResult(
        parsed_url.scheme, parsed_url.netloc, parsed_url.path,
        parsed_url.params, encoded_get_args, parsed_url.fragment
    ).geturl()
    return new_url

def get_url_params(url):
    parsed = urlparse(url)
    params = parse_qsl(parsed.query)
    return params

def generate_injection_payload():
    payload = ""

    while payload.count('\'') != 1 or payload.count('\"') != 1:
        payload = "".join(choice(HEURISTIC_CHECK_ALPHABET)
                          for _ in range(0, 10))
    return payload