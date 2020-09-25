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

import functools
import itertools
from pathlib import Path

here = Path(__file__).parent
properties_path = here / 'DerivedCoreProperties.txt'

# if the amount of shadowing builtins that i do bothers you, please fix your syntax highlighter / linter

def get_derived_core_properties():
	properties = {}

	with open(properties_path) as f:
		for property, range in parse_properties(f):
			properties.setdefault(property, set()).update(map(chr, range))

	return {property: frozenset(chars) for property, chars in properties.items()}

def get_derived_core_property(property):
	desired = property

	with open(properties_path) as f:
		for property, range in parse_properties(f):
			if property == desired:
				yield from map(chr, range)

def parse_properties(f):
	for line in map(str.strip, f):
		if line.startswith('#') or not line:
			continue

		# ignore trailing comments too
		line = ''.join(itertools.takewhile(lambda c: c != '#', line))

		range, property = map(str.strip, line.split(';'))

		range = unicode_range_to_range(range)
		yield property, range

def unicode_range_to_range(range_str):
	return inclusive_range(*map(hex_to_int, range_str.split('..')))

hex_to_int = functools.partial(int, base=16)

def inclusive_range(start, stop=None, step=1):
	return range(start, start + 1 if stop is None else stop + 1, step)

def main():
	with open(here / 'derived_core_properties.py', 'w') as f:
		f.write('# generated by gen_derived_core_properties.py\n')
		f.write("DEFAULT_IGNORABLE = frozenset('")
		for c in get_derived_core_property('Default_Ignorable_Code_Point'):
			f.write(c)
		f.write("')\n")

if __name__ == '__main__':
	main()