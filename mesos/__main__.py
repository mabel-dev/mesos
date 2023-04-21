#!/usr/bin/env python

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
A command line interface for Mesos
"""
import asyncio
import os
import sys

import typer

sys.path.insert(1, os.path.join(sys.path[0], "../../opteryx"))
sys.path.insert(1, os.path.join(sys.path[0], ".."))

import mesos  # isort: skip
from mysql_mimic import MysqlServer  # isort: skip
from mysql_mimic import Session  # isort: skip
from orso import logging  # isort: skip

logging.set_log_name("MESOS")
logger = logging.get_logger()
logger.setLevel(5)

# Define ANSI color codes
ANSI_RED = "\u001b[31m"
ANSI_BLUE = "\u001b[36m"
ANSI_RESET = "\u001b[0m"


class MySession(Session):
    async def query(self, sql, attrs):
        import opteryx  # isort: skip

        print(f"Original SQL string: {sql}")
        print(f"Query attributes: {attrs}")
        print(f"Currently authenticated user: {self.username}")
        print(f"Currently selected database: {self.database}")

        try:
            curr = opteryx.query(sql)
            return curr.fetchall(), curr.column_names
        except Exception as err:
            logger.exception(f"{type(err).__name__} - {err}")
            raise err


# fmt:off
def main():
# fmt:on
    print(f"{ANSI_BLUE}   ____ ___  ___  _________  _____")
    print("  / __ `__ \/ _ \/ ___/ __ \/ ___/")
    print(" / / / / / /  __(__  ) /_/ (__  ) ")
    print(f"/_/ /_/ /_/\___/____/\____/____/  {ANSI_RESET}")
    print(f"     mesos version {mesos.__version__}")
    server = MysqlServer(session_factory=MySession, port=3306)
    asyncio.run(server.serve_forever())


if __name__ == "__main__":  # pragma: no cover
    try:
        typer.run(main)
    except Exception as e:
        # Display a friendly error message if an exception occurs
        print(f"{ANSI_RED}Error{ANSI_RESET}: {e}")
