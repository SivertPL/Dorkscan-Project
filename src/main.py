#!/usr/bin/python3
import os
import asyncio
import argparse
import collect
import string
import curses
import datetime
import random
import html
import errorparse
import views 
import settings 

from util import progressbar, sort_urls, u_round
from urllib.parse import unquote
from scanner import scan_urls

loaded_dorks = []
all_dorks = [line.strip()
             for line in open("lists/list.txt", 'r', encoding='utf-8') if not line[0] == "#"]


def parse_arguments():
    parser = argparse.ArgumentParser(description='DorkScan is a tool used to find vulnerable websites based on search engine results')
    parser.add_argument('domain', help='Domain to look for ex. .com, .net, .org', type=str)
    parser.add_argument('quantity', help='Specifies how many dorks to use. 0 means all',type=int)
    parser.add_argument('--pages', help='Specifies how many search engine pages should be scanned per 1 dork [25-100]',type=int,const=25, nargs='?')
    parser.add_argument('--norandom', help='Do NOT choose the dorks randomly', action="store_true")
    parser.add_argument("--tor", help='Use TOR for anonymization purposes (127.0.0.1:9060)', action="store_true")
    parser.add_argument("--proxy", help="Full URL of a proxy, ex. socks5://127.0.0.1:9050", type=str)
    args = vars(parser.parse_args())

    if "." not in args["domain"]:
        print("Example: \".com\"")
        exit(0)
    if args["norandom"] is True:
        settings.RANDOM_ORDER = False
    if args["pages"] is not None:
        if int(args["pages"]) < 25 or int(args["pages"]) > 100:
            print("25-100 increments of 25")
            exit(0)
        settings.PAGES_PER_DORK = int(args["pages"])
    
    if args["tor"] is True:
        settings.TOR_ENABLED = True 
    
    settings.DOMAIN = args["domain"]
    settings.QUANTITY = args["quantity"]
    main()


def main():
    errorparse.parse_errors_file()
    stdscr = views.setup_curses()

    amount = settings.QUANTITY

    if amount == 0:
        loaded_dorks.extend(all_dorks)
    else: 
        if settings.RANDOM_ORDER:
            i = 0
            while i < amount:
                d = random.choice(all_dorks)
                loaded_dorks.append(d)
                i += 1
        else:
            i = 0
            while i < amount:
                d = all_dorks[i]
                loaded_dorks.append(d)
                i += 1
        pages = u_round(settings.PAGES_PER_DORK, base=25)
    
    eventloop = asyncio.get_event_loop()

    gathered_urls = eventloop.run_until_complete(
        collect.collect_urls(stdscr, loaded_dorks, settings.DOMAIN, int(pages)))
    gathered_urls = sort_urls(gathered_urls)

    stdscr.addstr(10, 1, "Success! Gathered {} urls".format(len(gathered_urls)), curses.color_pair(1))
    stdscr.addstr(11, 1, "Menu:")
    stdscr.addstr(12, 1, "1. Save them to a file (press V)")
    stdscr.addstr(13, 1, "2. Begin scanning (press S)")
    stdscr.addstr(14, 1, "3. Exit (press Q)")
    
    (lines, _) = stdscr.getmaxyx()
    lines -= 2
    
    while True:
        c = stdscr.getch()
        if c == ord('v'):
            save_file_name = 'collected/collected_' + \
                str(datetime.datetime.now().strftime(
                    '%Y_%m_%d_%H_%M_%S')) + '.svz'
            fhandle = open(save_file_name, "w+")
        
            for url in gathered_urls:
                fhandle.write(url + "\n")
            stdscr.addstr(16, 1, "Saved successfully! " + str(
                len(gathered_urls)) + " lines", curses.color_pair(1))
            
        if c == ord('q'):
            curses.nocbreak()
            stdscr.keypad(0)
            curses.echo()
            curses.endwin()
            exit(0)
        if c == ord('s'):
            stdscr.clear()
            future = asyncio.ensure_future(scan_urls(stdscr, gathered_urls))
            eventloop.run_until_complete(future)
            break 
        stdscr.addstr(lines, 1, "Dorkscan BETA https://github.com/SivertPL, press M for menu", curses.color_pair(3))
        stdscr.refresh()



if __name__ == "__main__":
    parse_arguments()