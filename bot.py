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
from random import random

import syncpg
from semaphore import Bot, ChatContext
import toml

import utils.shout
from db import Database

with open('config.toml') as f:
	config = toml.load(f)

import logging
bot = Bot(config['username'])
bot.config = config
logger = logging.getLogger(__name__)

@bot.handler()
def shout(ctx: ChatContext):
	msg = ctx.message

	if not utils.shout.is_shout(msg.get_body()):
		return

	group_id = msg.get_group_id()
	if not group_id:
		# this bot doesn't work in DMs but that doesn't mean we can't have a bit of fun
		msg.reply('KEEP YOUR VOICE DOWN')
		return

#		if not bot.db.state(group_id, msg.source):
#			print(2)
#			return

	# try to reduce spam
	if random() < config.get('shout_response_probability', 0.4):
		shout = bot.db.random_shout(group_id)
		msg.reply(shout or "I AIN'T GOT NOTHIN' ON THAT")

	bot.db.save_shout(msg)

def main():
	bot.db = Database(syncpg.connect(**bot.config['database']))
	bot.start()

if __name__ == '__main__':
	main()
