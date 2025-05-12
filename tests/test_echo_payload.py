#
# This file is part of the C1_echo_example_with_python_and_pika distribution
# (https://github.com/VALAWAI/C1_echo_example_with_python_and_pika).
# Copyright (c) 2022-2026 VALAWAI (https://valawai.eu/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import unittest
from pydantic import ValidationError
from c1_echo_example_with_python_and_pika.echo_payload import EchoPayload

class TestEchoPayload(unittest.TestCase):
	"""Class to test the echo payload"""

	def test_not_allow_define_empty_payload(self):
		"""Test can create an empty echo"""

		error = False
		try:

			echo = EchoPayload()
			assert echo is None

		except ValidationError:
			error = True

		# Can create empty echo
		assert error

	def test_fail_load_empty_json(self):
		"""Test can not load a echo from an empty json"""

		error = False
		try:

			json_value = {}
			echo = EchoPayload(**json_value)
			assert echo is None

		except ValidationError:
			error = True

		# Can create empty echo
		assert error


	def test_fail_load_echo_with_empty_content(self):
		"""Test can not load a echo with empty content"""

		error = False
		try:

			json_value = {"content":""}
			echo = EchoPayload(**json_value)
			assert echo is None

		except ValidationError:
			error = True

		# Can load a echo with empty id
		assert error
