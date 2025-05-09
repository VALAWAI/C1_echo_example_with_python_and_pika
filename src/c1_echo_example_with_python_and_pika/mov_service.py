#
# This file is part of the C2_treatment_autonomy_valuator distribution
# (https://github.com/VALAWAI/C2_treatment_autonomy_valuator).
# Copyright (c) 2022-2026 VALAWAI (https://valawai.eu/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. 	If not, see <http://www.gnu.org/licenses/>.
#
import json
import logging
import os.path
import re

from message_service import MessageService


class MOVService:
	"""The component used to interact with the Master Of VALAWAI (MOV)"""

	def __init__(self, message_service:MessageService):
		"""Initialize the MOV service

		Parameters
		----------
		message_service: MessageService
			The service to receive or send messages thought RabbitMQ
		"""
		self.message_service = message_service
		self.component_id = None

	def __read_file(self, path:str):
		"""Read a file and return its content."""

		class_file_path = os.path.abspath(os.path.dirname(__file__))
		file_path = os.path.join(class_file_path, path)
		with open(file_path) as file:
			return file.read()
			
	def load_default_project_version(self):
		"""Obtain the default version of the project"""
		setup = self.__read_file('../../pyproject.toml')
		version = re.findall(r"version\s*=\s*\"(\d+\.\d+\.\d+)\"", setup)[0]
		return version

	def load_default_asyncapi_yaml(self):
		"""Obtain the default AsyncAPI of the component"""
		async_api = self.__read_file('../../asyncapi.yaml')
		return async_api
		
	def extract_default_component_name(self,asyncapi_yaml:str):
		"""Obtain the default name of the component from the AsyncAPI description"""
		
		match = re.findall(r"valawai/(c[0|1|2]/\w+)/control/registered:", asyncapi_yaml)[0]
		return match[0:2] + '_' + match[3:]
		

	def listen_for_registered_component(self,name:str):
		""" The message to register this component into the MOV
			(https://valawai.github.io/docs/tutorials/mov#register-a-component)
		"""

		level = name[0:2].lower()
		name_without_level = name[3:].lower()
		self.message_service.listen_for(f'valawai/{level}/{name_without_level}/control/registered', self.registered_component)

	def register_component(self,name:str,version:str,asyncapi_yaml:str):
		""" Register this component into the MOV
			(https://valawai.github.io/docs/tutorials/mov#register-a-component)

		Parameters
		----------
		name: str
			The name of the component. This is the compoennt type plus the name of the component. 
			For example "c2_treatment_autonomy_valuator".
		version: str
			The version of the component.
		asyncapi_yaml: str
			The description of the component services in AsyncAPI as a string.
		"""

		level = name[0:2].upper()
		register_payload = {
			"type": level,
			"name": name,
			"version": version,
			"asyncapi_yaml": asyncapi_yaml
			}
		self.message_service.publish_to('valawai/component/register', register_payload)

	def registered_component(self, _ch, _method, _properties, body):
		"""Called when the component has been registered."""

		logging.debug("Received registered component %s", body)
		msg = json.loads(body)
		self.component_id = msg['id']
		logging.info("Register C2 Treatment autonomy valuator with the identifier '%s'",self.component_id)

		try:

			log_dir = os.getenv("LOG_DIR", "logs")
			if not os.path.exists(log_dir):

				os.makedirs(log_dir)

			component_id_path = os.path.join(log_dir, os.getenv("COMPONET_ID_FILE_NAME", "component_id.json"))
			with open(component_id_path, "w") as component_id_file:

				content = json.dumps(msg, sort_keys=True, indent=2)
				component_id_file.write(content)

		except (OSError, ValueError):

			logging.exception("Could not store the component id into a file")

	def unregister_component(self):
		""" Unregister this component from the MOV
			(https://valawai.github.io/docs/tutorials/mov/#unregister-a-component)
		"""
		try:

			log_dir = os.getenv("LOG_DIR", "logs")
			if os.path.exists(log_dir):

				component_id_path = os.path.join(log_dir, os.getenv("COMPONET_ID_FILE_NAME", "component_id.json"))
				if os.path.isfile(component_id_path):

					os.remove(component_id_path)

		except (OSError, ValueError):

			logging.exception("Could not remove previous component id file")

		if self.component_id is not None:

				msg = {"component_id":self.component_id}
				self.message_service.publish_to('valawai/component/unregister', msg)
				logging.info("Unregisterd C2 Treatment autonomy valuator with the identifier '%s'",self.component_id)
				self.component_id = None

	def debug(self, msg:str, payload=None):
		""" Send a debug log message to the MOV
			(https://valawai.github.io/docs/tutorials/mov/#add-a-log-message)

		Parameters
		----------
		msg : str
			The log message
		payload: object
			The payload associated to the log message.
		"""
		self.__log('DEBUG', msg, payload)
		logging.debug(msg)

	def info(self, msg:str, payload=None):
		""" Send a info log message to the MOV
			(https://valawai.github.io/docs/tutorials/mov/#add-a-log-message)

		Parameters
		----------
		msg : str
			The log message
		payload: object
			The payload associated to the log message.
		"""
		self.__log('INFO', msg, payload)
		logging.info(msg)

	def warn(self, msg:str, payload=None):
		""" Send a warn log message to the MOV
			(https://valawai.github.io/docs/tutorials/mov/#add-a-log-message)

		Parameters
		----------
		msg : str
			The log message
		payload: object
			The payload associated to the log message.
		"""
		self.__log('WARN', msg, payload)
		logging.warning(msg)

	def error(self, msg:str, payload=None):
		""" Send a error log message to the MOV
			(https://valawai.github.io/docs/tutorials/mov/#add-a-log-message)

		Parameters
		----------
		msg : str
			The log message
		payload: object
			The payload associated to the log message.
		"""
		self.__log('ERROR', msg, payload)
		logging.error(msg)

	def __log(self, level:str, msg:str, payload=None):
		""" Send a log message to the MOV
			(https://valawai.github.io/docs/tutorials/mov/#add-a-log-message)

		Parameters
		----------
		level : str
			The log level
		msg : str
			The log message
		payload: object
			The payload associated to the log message.
		"""

		msg = msg.replace("{"," ")
		add_log_payload = {"level":level, "message": msg}

		if payload is not None:

			add_log_payload["payload"] = json.dumps(payload)

		if self.component_id is not None:

			add_log_payload["component_id"] = self.component_id

		self.message_service.publish_to('valawai/log/add', add_log_payload)
