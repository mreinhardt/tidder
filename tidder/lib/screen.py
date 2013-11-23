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
    BAR = 2
    STATUSBAR = 3
    MESSAGEBAR = 4


class Screen(object):
    def __init__(self):
        global log
        try:
            curses.wrapper(self._main)
        except KeyboardInterrupt:
            log.clear_screen()

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

        self.bars = {
            'status': StatusBar(self),
            'message': MessageBar(self)
        }

        while True:
            c = self.stdscr.getch()
            ck = filter(lambda t: t[1] == c, curses.__dict__.items())
            c = ck[0][0] if len(ck) else unctrl(c)
            logger.debug(c)

            if c in ['KEY_RESIZE', 'ERR']:
                self.height, self.width = self.stdscr.getmaxyx()
                self.stdscr.clear()
                self.stdscr.refresh()
                for bar in self.bars.values():
                    bar.setpos()

            if c == 'q':
                log.clear_screen()
                break


class Bar(object):
    bgcolor = Color.WHITE
    fgcolor = Color.BLACK

    def __init__(self, screen, bgcolor=None, fgcolor=None):
        self.screen = screen
        self.height = 1
        self.width = screen.width
        self.window = curses.newwin(self.height, self.width, 0, 0)
        if bgcolor is not None and fgcolor is not None:
            self.bgcolor = bgcolor
            self.fgcolor = fgcolor

        color_pair = getattr(ColorPair, self.__class__.__name__.upper())
        curses.init_pair(color_pair, self.fgcolor, self.bgcolor)

        self.window.bkgd(curses.color_pair(color_pair))
        self.setpos()

    def _repos(self):
        self.window.mvwin(self.y, self.x)
        self.window.refresh()

    def setpos(self):
        self.y = 0
        self.x = 0
        self.width = self.screen.width
        self._repos()

    def setstr(self, s):
        try:
            self.window.addstr(0, 0, "{0:<{1}}".format(s, self.width - 1))
            self.window.refresh()
        except:
            pass  # resizing terminal window, width incorrect


class StatusBar(Bar):
    bgcolor = Color.BRGREEN
    fgcolor = Color.BLACK

    def setpos(self):
        self.y = self.screen.height - 2
        self.x = 0
        self.width = self.screen.width
        self._repos()


class MessageBar(Bar):
    bgcolor = Color.BLACK
    fgcolor = Color.BRGREEN

    def __init__(self, screen, bgcolor=None, fgcolor=None):
        super(MessageBar, self).__init__(screen, bgcolor, fgcolor)

        self.window.addstr(0, 0, "Welcome to tidder!")
        self.window.refresh()

    def setpos(self):
        self.y = self.screen.height - 1
        self.x = 0
        self.width = self.screen.width
        self._repos()
