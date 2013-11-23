import inspect
import logging


_config = None


class ScreenHandler(logging.StreamHandler):
    """A handler class which outputs log messages to curses screen."""

    def __init__(self, screen, *args, **kwargs):
        self.screen = screen
        super(ScreenHandler, self).__init__(*args, **kwargs)

    def emit(self, record):
        try:
            msg = self.format(record)
            self.screen.status_bar.setstr(msg)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


class Log(object):
    def __init__(self, level=None, filename=None):
        global _config
        if level is None and _config is not None:
            self.__dict__ = _config.copy()

        elif level is None:
            raise ValueError('Missing log level')

        else:
            numeric_level = getattr(logging, level.upper(), None)
            if not isinstance(numeric_level, int):
                raise ValueError('Invalid log level: {0}'.format(level))
            self.level = numeric_level
            self.filename = filename
            self.screen = None
            self.format = '%(asctime)s, %(name)s, %(levelname)s: %(message)s'
            self.datefmt = '%Y-%m-%d %I:%M:%S%p'
            self._set_config()

        self.logger = self._get_logger()

    def _set_config(self):
        global _config
        _config = self.__dict__.copy()
        logging.basicConfig(**_config)

    def _get_logger(self):
        caller = inspect.stack()[2]
        module = inspect.getmodule(caller[0])
        return logging.getLogger(module.__name__)

    def set_screen(self, screen):
        self.screen = screen
        self._set_config()
        self.screen_handler = ScreenHandler(screen)
        self.screen_handler.setFormatter(
            logging.Formatter(fmt=self.format, datefmt=self.datefmt))
        self.screen_handler.setLevel(self.level)
        self.logger.propagate = False
        self.logger.addHandler(self.screen_handler)

    def clear_screen(self):
        self.screen = None
        self.logger.removeHandler(self.screen_handler)
        self.logger.propagate = True
        self._set_config()
