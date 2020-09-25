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
import uuid

import jinja2

class Database:
	def __init__(self, conn):
		self.conn = conn
		with open('queries.sql') as f:
			self.queries = jinja2.Template(f.read(), line_statement_prefix='-- :').module

	def save_shout(self, message):
		group_id = base64.b64decode(message.get_group_id())
		tag = self.conn.execute(self.queries.save_shout(), group_id, message.get_body())
		return tag == 'INSERT 0 1'

	# some terminology: a "chat_id" is a group chat UUID
	# a "peer_id" is either a chat_id or a user_id (also a UUID)

	def random_shout(self, chat_id):
		return self.conn.fetchval(self.queries.random_shout(), base64.b64decode(chat_id))

	def delete_shout(self, chat_id, content):
		tag = self.conn.execute(self.queries.delete_shout(), base64.b64decode(chat_id), content)
		return int(tag.split()[-1])

	def delete_by_chat(self, chat_id):
		tag = self.conn.execute(self.queries.delete_by_chat(), base64.b64decode(chat_id))
		return int(tag.split()[-1])

	def state_for(self, peer_id):
		return self.conn.fetchval(self.queries.state_for(), peer_id)

	def toggle_state(self, peer_id, *, default_new_state=False):
		"""toggle the state for a user or chat. If there's no entry already, new state = default_new_state."""
		return self.conn.fetchval(self.queries.toggle_state(), peer_id, default_new_state)

	def set_state(self, peer_id, new_state):
		self.conn.execute(self.queries.set_state(), peer_id, new_state)

	def toggle_user_state(self, user_id, chat_id=None) -> bool:
		"""Toggle whether the user has opted in to the bot.
		If the user does not have an entry already:
			If the chat_id is provided and not None, the user's state is set to the opposite of the chat's.
			Otherwise, the user's state is set to True (opted in), since the default state is False.
		Returns the new state.
		"""
		default_new_state = False
		chat_state = self.state_for(base64.b64decode(chat_id)) if chat_id is not None else default_new_state
		if chat_state is not None:
			# if the auto response is enabled for the chat then toggling the user state should opt out
			default_new_state = not chat_state
		return self.toggle_state(user_id, default_new_state=default_new_state)

	def state(self, chat_id, user_id):
		return self.conn.fetchval(self.queries.state(), base64.b64decode(chat_id), user_id)
