import argparse
from os import path
import re


class Settings(object):
    def __init__(self):
        self.config = self._read_config()
        self.argparser = self._init_parser()
        self.args = self.parse_args()
        self.settings = self.create_settings()

    def _read_config(self):
        config_filename = '.tidderrc'
        try:
            filename = path.join(path.expanduser('~'), config_filename)
            with open(filename) as config_file:
                return self._read_config_file(config_file.readlines())
        except IOError as e:
            return {}

    def _read_config_file(self, raw_config):
        config_pattern = re.compile(r'(\w+)=(.*)')
        config = {}
        for line in raw_config:
            m = config_pattern.match(line)
            if m is not None:
                k, v = m.groups()
                config[k] = v
        return config

    def _init_parser(self):
        argparser = argparse.ArgumentParser(
            description='"I dunno, just put the word \'description\'."',
            usage='bin/tidder')
        argparser.add_argument('-u', '--username', help='username')
        argparser.add_argument('-p', '--password', help='password')
        return argparser

    def parse_args(self):
        return self.argparser.parse_args()

    def create_settings(self):
        settings = {}
        args = self.args.__dict__
        settings.update(args)  # ensure defaults
        settings.update(self.config)
        settings.update({k:v for k,v in args.iteritems() if v is not None})
        return settings
