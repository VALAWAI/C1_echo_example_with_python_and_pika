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

import logging
import os
import sys

test_path = os.path.dirname(os.path.realpath(__file__))
if test_path not in sys.path:
    sys.path.append(test_path)

logging.basicConfig(filename='.test.log', level=logging.DEBUG)
