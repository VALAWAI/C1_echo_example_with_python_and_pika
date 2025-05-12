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
import uuid
import time
import logging
import json
from c1_echo_example_with_python_and_pika.message_service import MessageService
from c1_echo_example_with_python_and_pika.mov_service import MOVService
from c1_echo_example_with_python_and_pika.echo_handler import EchoHandler
from c1_echo_example_with_python_and_pika.echo_payload import EchoPayload

class TestEchoHandler(unittest.TestCase):
	"""Class to test the manage of tehreceived messages to echoed."""

	@classmethod
	def setUpClass(cls):
		"""Create the handler."""

		cls.message_service = MessageService()
		cls.mov = MOVService(cls.message_service)
		cls.handler = EchoHandler(cls.message_service, cls.mov)
		cls.msgs = []
		cls.message_service.listen_for('valawai/c1/echo_example_with_python_and_pika/data/publish_message', cls.callback)
		cls.message_service.start_consuming_and_forget()

	@classmethod
	def tearDownClass(cls):
		"""Stops the message service."""

		cls.mov.unregister_component()
		cls.message_service.close()

	@classmethod
	def callback(cls, _ch, _method, _properties, body):
		"""Called when a message is received from a listener."""

		try:

			logging.debug("Received %s", body)
			msg = json.loads(body)
			cls.msgs.append(msg)

		except ValueError:

			logging.exception("Unexpected %s", body)

			
	def test_handle_echo_message(self):
		"""Check that a message is echoed."""

		expected_content = str(uuid.uuid4())
		payload = {
			"content": expected_content
		}
		self.message_service.publish_to('valawai/c1/echo_example_with_python_and_pika/data/received_message', payload)
		for _i in range(10):

			for msg in self.msgs:

				if 'content' in msg and msg['content'] == expected_content:
					# Received the echoed message
					return

			time.sleep(3)

		self.fail("Not echoed message")
