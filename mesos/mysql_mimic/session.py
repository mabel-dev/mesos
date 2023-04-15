from __future__ import annotations

import typing
from contextlib import contextmanager

from mysql_mimic.results import AllowedResult
from mysql_mimic.variables import GlobalVariables
from mysql_mimic.variables import SessionVariables
from mysql_mimic.variables import Variables

if typing.TYPE_CHECKING:
    from mysql_mimic.connection import Connection

    Interceptor = typing.Callable


class BaseSession:
    """
    Session interface.

    This defines what the Connection object depends on.

    Most applications to implement the abstract `Session`, not this class.
    """

    variables: Variables
    username: typing.Optional[str]
    database: typing.Optional[str]

    async def query(self, sql: str, attrs: typing.Dict[str, str]) -> AllowedResult:
        """
        Main entrypoint for queries.

        Args:
            sql: SQL statement
            attrs: Mapping of query attributes
        Returns:
            One of:
            - tuple(rows, column_names), where "rows" is a sequence of sequences
              and "column_names" is a sequence of strings with the same length
              as every row in "rows"
            - tuple(rows, result_columns), where "rows" is the same
              as above, and "result_columns" is a sequence of mysql_mimic.ResultColumn
              instances.
            - mysql_mimic.ResultSet instance
        """

    async def init(self, connection: Connection) -> None:
        """
        Called when connection phase is complete.
        """

    async def close(self) -> None:
        """
        Called when the client closes the connection.
        """

    async def reset(self) -> None:
        """
        Called when a client resets the connection and after a COM_CHANGE_USER command.
        """

    async def use(self, database: str) -> None:
        """
        Use a new default database.

        Called when a USE database_name command is received.

        Args:
            database: database name
        """


class Session(BaseSession):
    """
    Abstract session.

    This automatically handles lots of behavior that many clients except,
    e.g. session variables, SHOW commands, queries to INFORMATION_SCHEMA, and more
    """

    def __init__(self, variables: Variables | None = None):
        self.variables = variables or SessionVariables(GlobalVariables())


        # Current authenticated user
        self.username = None

        self._connection: typing.Optional[Connection] = None

    async def query(self, sql: str = "", attrs: typing.Dict[str, str] = None) -> AllowedResult:
        """
        Process a SQL query.

        Args:
            sql: original SQL statement from client
            attrs: arbitrary query attributes set by client
        Returns:
            One of:
            - tuple(rows, column_names), where "rows" is a sequence of sequences
              and "column_names" is a sequence of strings with the same length
              as every row in "rows"
            - tuple(rows, result_columns), where "rows" is the same
              as above, and "result_columns" is a sequence of mysql_mimic.ResultColumn
              instances.
            - mysql_mimic.ResultSet instance
        """
        return [], []

    async def schema(self) -> dict | BaseInfoSchema:
        """
        Provide the database schema.

        This is used to serve INFORMATION_SCHEMA and SHOW queries.

        Returns:
            One of:
            - Mapping of:
                {table: {column: column_type}} or
                {db: {table: {column: column_type}}} or
                {catalog: {db: {table: {column: column_type}}}}
            - Instance of `BaseInfoSchema`
        """
        return {}

    @property
    def connection(self) -> Connection:
        """
        Get the connection associated with this session.
        """
        if self._connection is None:
            raise AttributeError("Session is not yet bound")
        return self._connection

    async def init(self, connection: Connection) -> None:
        """
        Called when connection phase is complete.
        """
        self._connection = connection

    async def close(self) -> None:
        """
        Called when the client closes the connection.
        """
        self._connection = None
