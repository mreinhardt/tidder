import praw

from .. import VERSION


user_agent = 'User-Agent: tidder/{0} by mVChr'.format(VERSION)
api = praw.Reddit(user_agent=user_agent)
print user_agent
