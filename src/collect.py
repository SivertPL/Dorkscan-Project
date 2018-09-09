import main
import asyncio
import re
import requests
import curses
import html
import settings 

from urllib.parse import unquote 
from util import progressbar, fire_and_forget

async def collect_urls(stdscr, alldorks, domain, page_amount):
    urls_collected = []

    stdscr.border()
    stdscr.addstr(1, 1, "Collecting dorks...")

    quantity = 0
    for dork in alldorks:
        quantity += 1
        page = 0
        while page < int(page_amount):
            futures = []
            search_query = dork + "+site:" + domain
            loop = asyncio.get_event_loop()
            for i in range(25):
                complete_url = "http://www.bing.com/search?q=" + search_query + \
                    "&go=Submit&first=" + \
                        str((page + i) * 50 + 1) + "&count=50"
                futures.append(loop.run_in_executor(
                    None, fire_and_forget, complete_url))
            page += 25
        string_regex = re.compile('(?<=href=")(.*?)(?=")')
        names = []
        for future in futures:
            result = await future
            names.extend(string_regex.findall(result))
        domains = set()
        for name in names:
            basename = re.search(r"(?<=(://))[^/]*(?=/)", name)
            if (basename is None):
                basename = re.search(r"(?<=://).*", name)
            if basename is not None:
                basename = basename.group(0)
            if basename not in domains and basename is not None and name.startswith("http://"):
                domains.add(basename)
                urls_collected.append(unquote(html.unescape(name)))
        percent = int(quantity / len(alldorks) * 100)

        stdscr.addstr(2, 1, "Processed dorks: ({}/{}) for domain {}".format(quantity, len(alldorks), domain))
        stdscr.addstr(3, 1, "Current dork: {}".format(dork))
        stdscr.addstr(4, 1, "Collected URLs: {}".format(len(urls_collected)))
        stdscr.addstr(5, 1, "Progress: {} ({}%)".format(progressbar(quantity, len(alldorks)), percent))
        stdscr.addstr(7, 1, "Collecting mode: {}".format("random" if settings.RANDOM_ORDER else "sequential"))
        stdscr.refresh()
        stdscr.timeout(30)
    return urls_collected
