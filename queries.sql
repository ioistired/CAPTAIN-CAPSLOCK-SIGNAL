-- Copyright © io mintz <io@mintz.cc>
--
-- CAPTAIN CAPSLOCK is free software: you can redistribute it and/or modify
-- it under the terms of the GNU Affero General Public License as published
-- by the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- CAPTAIN CAPSLOCK is distributed in the hope that it will be fun,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
-- GNU Affero General Public License for more details.
--
-- You should have received a copy of the GNU Affero General Public License
-- along with CAPTAIN CAPSLOCK. If not, see <https://www.gnu.org/licenses/>.

-- :macro delete_shout()
-- params: chat_id, content
DELETE FROM shout
WHERE (chat_id, content) = ($1, $2)
-- :endmacro

-- :macro save_shout()
-- params: chat_id, message_id, content
INSERT INTO shout (chat_id, content)
VALUES ($1, $2)
ON CONFLICT DO NOTHING
-- :endmacro

-- :macro random_row_pred(table, pred)
FROM {{ table }}
WHERE {{ pred }}
OFFSET FLOOR(RANDOM() * (
	SELECT COUNT(*)
	FROM {{ table }}
	WHERE {{ pred }}
))
FETCH FIRST ROW ONLY
-- :endmacro

-- :macro random_shout()
-- params: chat_id
SELECT content
{{ random_row_pred('shout', 'chat_id = $1') }}
-- :endmacro

-- :macro delete_by_chat()
-- params: chat_id
DELETE FROM shout
WHERE chat_id = $1
-- :endmacro

-- :macro state_for()
-- params: peer_id
SELECT state
FROM opt
WHERE peer_id = $1
-- :endmacro

-- :macro state()
-- params: chat_id, user_id
SELECT COALESCE(
	(SELECT state FROM opt WHERE peer_id = $2),
	(SELECT state FROM opt WHERE peer_id = $1),
	true) -- default state
-- :endmacro

-- :macro toggle_state()
-- params: peer_id, default_new_state
-- returns: new state
INSERT INTO opt (peer_id, state) VALUES ($1, $2)
ON CONFLICT (peer_id) DO UPDATE
SET state = NOT opt.state
RETURNING state
-- :endmacro

-- :macro set_state()
-- params: peer_id, new_state
INSERT INTO opt (peer_id, state)
VALUES ($1, $2)
ON CONFLICT (peer_id) DO UPDATE
SET state = EXCLUDED.state
-- :endmacro
