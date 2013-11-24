import praw

from .. import VERSION
from tidder.lib.log import Log


logger = Log().logger


user_agent = 'User-Agent: tidder/{0} by mVChr'.format(VERSION)
api = praw.Reddit(user_agent=user_agent, disable_update_check=True)
logger.debug(user_agent)
