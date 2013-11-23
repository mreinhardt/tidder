import inspect
import logging


_config = None


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
