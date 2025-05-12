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

import json
import logging
import os

from echo_payload import EchoPayload
from message_service import MessageService
from mov_service import MOVService
from pydantic import ValidationError


class EchoHandler:
	"""The component that receive mesages and echoed tehm.
	"""

	def __init__(self,message_service:MessageService,mov:MOVService):
		"""Initialize the handler

		Parameters
		----------
		message_service : MessageService
				The service to receive or send messages thought RabbitMQ
		mov : MOVService
				The service to interact with the MOV
		"""
		self.message_service = message_service
		self.mov = mov
		self.message_service.listen_for('valawai/c1/echo_example_with_python_and_pika/data/received_message',self.handle_message)


	def handle_message(self, _ch, _method, _properties, body):
		"""Manage the received messages on the channel valawai/c1/echo_example_with_python_and_pika/data/received_message
		"""

		try:

			json_dict = json.loads(body)

			try:

				payload = EchoPayload(**json_dict)
				self.mov.info("Received a message to echo",json_dict)

				echoed_msg = {
						"content": payload.content
					}
				self.message_service.publish_to('valawai/c1/echo_example_with_python_and_pika/data/publish_message',echoed_msg)
				self.mov.info("Sent Echoed message",echoed_msg)

			except ValidationError as validation_error:

				msg = f"Cannot process echo, because {validation_error}"
				self.mov.error(msg,json_dict)

		except ValueError:

			logging.exception("Unexpected message %s",body)
