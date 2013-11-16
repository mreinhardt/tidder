import argparse


class Settings(object):
    def __init__(self):
        self._init_args()

    def _init_args(self):
        self.parser = argparse.ArgumentParser(
            description='"I dunno, just put the word \'description\'."',
            usage='bin/tidder')
        self.parser.add_argument('-u', '--username', help='username')
        self.parser.add_argument('-p', '--password', help='password')

    def parse_args(self):
        self.args = self.parser.parse_args()
