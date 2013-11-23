"""
    tidder
    Copyright (C) 2013  Mike Reinhardt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from praw.errors import InvalidUserPass

from lib.log import Log


def main(settings):
    log = Log(level=settings['log'] or 'WARNING')
    logger = log.logger

    from lib.screen import Screen
    from reddit.auth import login

    try:
        if (settings['username'] is not None and
            settings['password'] is not None):
            login(settings['username'], settings['password'])
    except InvalidUserPass as e:
        log.logger.error('Incorrect password')

    screen = Screen()
    logger.info("tidder!")
    logger.debug(settings)
