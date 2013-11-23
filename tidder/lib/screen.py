import curses

from tidder.lib.log import Log


logger = Log().logger


class Screen(object):
     def __init__(self):
          try:
               curses.wrapper(self._main)
          except KeyboardInterrupt:
               logger.info("Goodbye tidder, hello life...")
               exit()

     def _main(self, stdscr):
          self.stdscr = stdscr

          # curses experimentation
          curses.start_color()
          curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
          curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

          self.stdscr.bkgd(curses.color_pair(1))
          self.stdscr.refresh()

          self.height, self.width = self.stdscr.getmaxyx()

          win = curses.newwin(6, 20, self.height / 2 - 3, self.width / 2 - 10)
          win.bkgd(curses.color_pair(2))
          win.box()
          win.attron(curses.A_BOLD)
          win.addstr(2, 2, "tidder!")
          win.refresh()

          while True:
               c = self.stdscr.getch()
               win.addstr(3, 2, "{0:<15}".format(c))
               win.refresh()
               if c in [curses.KEY_RESIZE, curses.ERR]:
                    self.height, self.width = self.stdscr.getmaxyx()
                    win.mvwin(self.height / 2 - 3, self.width / 2 - 10)
                    self.stdscr.clear()
                    self.stdscr.refresh()
                    win.refresh()
               if c == ord('q'):
                    break
