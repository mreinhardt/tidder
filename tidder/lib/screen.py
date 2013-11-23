import curses
from curses.ascii import unctrl

from tidder.lib.log import Log


log = Log()
logger = log.logger


class Color(object):
    BLACK = curses.COLOR_BLACK
    BLUE = curses.COLOR_BLUE
    CYAN = curses.COLOR_CYAN
    GREEN = curses.COLOR_GREEN
    MAGENTA = curses.COLOR_MAGENTA
    RED = curses.COLOR_RED
    WHITE = curses.COLOR_WHITE
    YELLOW = curses.COLOR_YELLOW
    BRBLACK = 8
    BRRED = 9
    BRGREEN = 10
    BRYELLOW = 11
    BRBLUE = 12
    BRMAGENTA = 13
    BRCYAN = 14
    BRWHITE = 15


class ColorPair(object):
    SCREEN = 1
    STATUSBAR = 3


class Screen(object):
    def __init__(self):
        global log
        try:
            curses.wrapper(self._main)
        except KeyboardInterrupt:
            log.clear_screen()
            logger.info("Goodbye tidder, hello life...")
            exit()

    def _main(self, stdscr):
        global log
        log.set_screen(self)

        self.stdscr = stdscr

        curses.start_color()
        color_pair = getattr(ColorPair, self.__class__.__name__.upper())
        curses.init_pair(color_pair, curses.COLOR_BLUE, curses.COLOR_BLACK)

        self.stdscr.bkgd(curses.color_pair(color_pair))
        self.stdscr.refresh()

        self.height, self.width = self.stdscr.getmaxyx()

        self.status_bar = StatusBar(1, self.width, self.height - 2, 0)

        while True:
            c = self.stdscr.getch()
            ck = filter(lambda t: t[1] == c, curses.__dict__.items())
            c = ck[0][0] if len(ck) else unctrl(c)
            logger.debug(c)

            if c in ['KEY_RESIZE', 'ERR']:
                self.height, self.width = self.stdscr.getmaxyx()
                self.status_bar.width = self.width
                self.status_bar.window.mvwin(self.height - 2, 0)
                self.stdscr.clear()
                self.stdscr.refresh()
                self.status_bar.window.refresh()

            if c == 'q':
                log.clear_screen()
                break


class StatusBar(object):
    bgcolor = Color.BRGREEN
    fgcolor = Color.BLACK

    def __init__(self, height, width, y, x, bgcolor=None, fgcolor=None):
        self.y = y
        self.x = x
        self.height = height
        self.width = width
        self.window = curses.newwin(height, width, y, x)
        if bgcolor is not None and fgcolor is not None:
            self.bgcolor = bgcolor
            self.fgcolor = fgcolor

        color_pair = getattr(ColorPair, self.__class__.__name__.upper())
        curses.init_pair(color_pair, self.fgcolor, self.bgcolor)

        self.window.bkgd(curses.color_pair(color_pair))
        self.window.addstr(0, 0, "Welcome to tidder!")
        self.window.refresh()

    def setstr(self, s):
        self.window.addstr(0, 0, "{0:<{1}}".format(s, self.width - 1))
        self.window.refresh()
