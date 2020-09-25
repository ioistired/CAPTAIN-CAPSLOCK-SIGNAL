#!/usr/bin/env python3

# Copyright © io mintz <io@mintz.cc>
#
# CAPTAIN CAPSLOCK is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CAPTAIN CAPSLOCK is distributed in the hope that it will be fun,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with CAPTAIN CAPSLOCK. If not, see <https://www.gnu.org/licenses/>.

import base64
import logging
from functools import wraps
from random import random
from typing import Optional

import syncpg
from semaphore import Bot, ChatContext, Reply
import toml

import utils.shout
from db import Database

with open('config.toml') as f:
	config = toml.load(f)

bot = Bot(config['username'])
bot.config = config
logger = logging.getLogger(__name__)

def handler(pattern=''):
	if callable(pattern):
		func = pattern
		return handler('')(func)

	def deco(func):
		@wraps(func)
		def wrapped(ctx: ChatContext) -> Optional[Reply]:
			try:
				return func(ctx)
			except Exception as e:
				logger.error('Ignoring exception in %s', func.__name__, exc_info=e)

		bot.register_handler(pattern, wrapped)
		return wrapped
	return deco

@handler
def shout(context: ChatContext) -> Optional[Reply]:
	msg = context.message

	if not utils.shout.is_shout(msg.get_body()):
		return

	group_id = msg.get_group_id()
	if not group_id:
		# this bot doesn't work in DMs but that doesn't mean we can't have a bit of fun
		return Reply(body='KEEP YOUR VOICE DOWN')

#		if not bot.db.state(group_id, msg.source):
#			print(2)
#			return

	reply = None

	# try to reduce spam
	if random() < 1:
		shout = bot.db.random_shout(group_id)
		reply = Reply(body=shout or "I AIN'T GOT NOTHIN' ON THAT")

	bot.db.save_shout(msg)
	return reply

def main():
	bot.db = Database(syncpg.connect(**bot.config['database']))
	bot.start()

if __name__ == '__main__':
	main()
