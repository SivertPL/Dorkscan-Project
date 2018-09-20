import urllib
import xml.dom.minidom 
import urllib.parse as urlparse
import xml.etree.ElementTree
import re 
import asyncio, aiohttp 
import main
import curses, datetime 
import settings 
import proxy 

from errorparse import add_url_params, generate_injection_payload, check_error_present, get_url_params
from aiohttp import ClientSession

errors = []
checked = 0

## TODO: Add LFI support, CheckedUrl object

async def check_url(session, url, which, stdscr):
    params = get_url_params(url)
    global checked

    for (key, value) in params:
        aug_value = value + generate_injection_payload()
        aug_url = add_url_params(url, dict([(key, aug_value)]))
        try:
            timeout = aiohttp.ClientTimeout(total=settings.SCAN_REQUEST_TIMEOUT)
            session_kwargs = {'timeout': timeout}

            if proxy.is_proxied():
                session_kwargs['proxy'] = proxy.get_proxy_url()

            async with session.get(aug_url, **session_kwargs) as response_object:
                response = await response_object.text() 
                err = check_error_present(response)
                if err:
                    errors.append(aug_url)
                    return True
        except Exception as e:
            #print("Exception at {}".format(checked))
            continue
    if checked % 10 == 1:
            stdscr.addstr(2, 1, "Processed urls: {}".format(checked))
            stdscr.refresh()
    checked += 1
    return False


async def scan_urls(stdscr, urls):
    result = []
    tasks = []
    stdscr.border()
    stdscr.addstr(1, 1, "Scanning URLs for SQL injection...")
    stdscr.addstr(3, 1, "Please be patient, it's working")
    stdscr.addstr(4, 1, "Proxy: {}".format("enabled" if proxy.is_proxied() else "disabled"))

    connector = aiohttp.TCPConnector(limit=len(urls))
    async with aiohttp.ClientSession(connector=connector) as session:
        q = 0
        for url in urls:
            task = asyncio.ensure_future(check_url(session, url, q, stdscr))
            tasks.append(task)
            q += 1
        result = await asyncio.gather(*tasks)

    (lines, _) = stdscr.getmaxyx()
    lines -= 2
    stdscr.addstr(5, 1, "Found {} vulnerable urls".format(len(errors)), curses.color_pair(1))
    stdscr.addstr(6, 1, "Menu:")
    stdscr.addstr(7, 1, "1. Save them to a file (press V)")
    stdscr.addstr(8, 1, "2. Go back to main menu (press B)")
    stdscr.addstr(9, 1, "3. Print them on screen (press P)")
    stdscr.addstr(10, 1, "4. Exit (press Q)")
    stdscr.addstr(lines, 1, "Dorkscan BETA https://github.com/SivertPL, press M for menu", curses.color_pair(3))
    stdscr.refresh()
    while True:
        c = stdscr.getch()
        if c == ord('v'):
            save_file_name = 'collected/vulnerable_' + \
                str(datetime.datetime.now().strftime(
                    '%Y_%m_%d_%H_%M_%S')) + '.svz'
            fhandle = open(save_file_name, "w+")
        
            for url in errors:
                fhandle.write(url + "\n")
            stdscr.addstr(12, 1, "Saved successfully! " + str(
                len(errors)) + " lines", curses.color_pair(1))
        if c == ord('q'):
            curses.nocbreak()
            stdscr.keypad(0)
            curses.echo()
            curses.endwin()
            exit(0)
        if c == ord('p'):
            stdscr.clear()
            i = 1
            for e in errors:
                if i < 15:
                    stdscr.addstr(i, 1, e)
                    i += 1
        if c == ord('b'):
            stdscr.clear()
            #main.gather(stdscr)
        stdscr.refresh()
    return result

