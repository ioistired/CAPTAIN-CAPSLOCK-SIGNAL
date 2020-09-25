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

IGNORED_WORDS = frozenset({
	'OK',
	'XD',
	'DX',
	'XP',
	'X-D',
	'D-X',
	'X-P',
	'P-X',
	'OwO',
	'UwU',
	'TIL',
})

def is_shout(str):
	# This import is done here because this is the __init__ file,
	# which is run when utils.shout.gen_derived_core_properties is run.
	# If this import were at the top level, the code generator would not be able to run
	# without the file that it generates.
	from .derived_core_properties import DEFAULT_IGNORABLE

	if str in IGNORED_WORDS:
		return False

	length = len(str)
	count = 0

	for c in str:
		if c.isspace() or c in DEFAULT_IGNORABLE:
			length -= 1
		if c.isupper():
			count += 1

	return length > 1 and count / length > 0.5
