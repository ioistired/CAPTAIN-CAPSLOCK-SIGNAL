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

import sys

from utils.shout import is_shout

while True:
	try:
		sentence = input('📣 ')
	except (KeyboardInterrupt, EOFError):
		print()
		break

	if not sys.stdin.isatty():
		print(sentence)
	print(is_shout(eval(sentence)))
