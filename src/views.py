import curses

def setup_curses():
    stdscr = curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, 0)
    curses.init_pair(2, curses.COLOR_MAGENTA, 0)
    curses.init_pair(3, curses.COLOR_YELLOW, 0)
    curses.init_pair(4, curses.COLOR_RED, 0)
    curses.init_pair(5, curses.COLOR_BLUE, 0)
    curses.curs_set(0)
    curses.noecho()
    stdscr.clear()
    return stdscr

## UNUSED
def greeting(stdscr):
    stdscr.border()
    add_center_text(stdscr, "Dorkscan", curses.color_pair(4) | curses.A_BOLD)
    add_center_text(stdscr, "Dork-based vulnerability scanner for all your skiddie needs",  offset_y=1)
    add_center_text(stdscr, "MENU", curses.color_pair(5) | curses.A_BOLD, offset_y=3)
    add_center_text(stdscr, "Quick scan [press B]", offset_y=4)
    add_center_text(stdscr, "About / Info [press A]", offset_y=5)
    add_center_text(stdscr, "Exit [press Q]", offset_y=6)
    stdscr.refresh()

## UNUSED
def add_center_text(stdscr, text, *posargs, bordered=True, offset_y=0, offset_x=0):
    (lines, columns) = stdscr.getmaxyx()
    s_len = len(text)
    middle_l = int(lines / 2) - 2 if bordered else int(lines / 2)
    middle_c = int(columns / 2 - s_len / 2)
    
    stdscr.addstr(middle_l + offset_y, middle_c + offset_x, text, *posargs)

    
