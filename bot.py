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

import anyio
import asyncpg
from semaphore import Bot, ChatContext
import toml

import utils.shout
from db import Database

async def shout(ctx: ChatContext):
	msg = ctx.message

	if not utils.shout.is_shout(msg.get_body()):
		return

	group_id = msg.get_group_id()
	if not group_id:
		# this bot doesn't work in DMs but that doesn't mean we can't have a bit of fun
		await msg.reply('KEEP YOUR VOICE DOWN')
		return

	# try to reduce spam
	if random() < ctx.bot.config.get('shout_response_probability', 0.4):
		shout = await ctx.bot.db.random_shout(group_id)
		await msg.reply(shout or "I AIN'T GOT NOTHIN' ON THAT")

	await ctx.bot.db.save_shout(msg)

async def main():
	with open('config.toml') as f:
		config = toml.load(f)

	import logging
	# shockingly, this is really how the docs want you doing it
	log_level = getattr(logging, config.get('log_level', 'INFO').upper(), None)
	if not isinstance(log_level, int):
		import sys
		logging.basicConfig(level=logging.ERROR)
		logging.error('Invalid log level %s specified!', log_level)
		sys.exit(1)
	else:
		logging.basicConfig(level=log_level)

	async with Bot(config['username'], socket_path=config.get('signald_socket_path', '/var/run/signald/signald.sock')) as bot:
		bot.register_handler('', shout)
		bot.config = config
		bot.db = Database(await asyncpg.create_pool(**bot.config['database']))
		await bot.start()

if __name__ == '__main__':
	anyio.run(main)
