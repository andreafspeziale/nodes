from sqlite3 import connect, Row, Connection
from logging import Logger
from typing import Optional


class DatabaseOpenConnectionException(Exception):
    pass


class DatabaseCloseConnectionException(Exception):
    pass


class Database:
    def __init__(self, logger: Logger, database_path: str):
        self.logger = logger
        try:
            self.connection = connect(database_path, check_same_thread=False)
            self.connection.row_factory = Row
        except Exception as e:
            self.logger.error(
                "An error occurred while establishing database connection: %s", e
            )
            raise DatabaseOpenConnectionException(
                "An error occurred while establishing database connection"
            ) from e

    def get_connection(self, database_path: Optional[str] = None) -> Connection:
        self.logger.debug("Retrieving database connection...")
        try:
            if self.connection is None:
                self.connection = connect(database_path, check_same_thread=False)
                self.connection.row_factory = Row
        except Exception as e:
            self.logger.error(
                "An error occurred while establishing database connection: %s", e
            )
            raise DatabaseOpenConnectionException(
                "An error occurred while establishing database connection"
            ) from e
        return self.connection

    # TODO: make some tests about closing the connection
    def close(self):
        self.logger.debug("Closing database connection...")
        try:
            if self.connection is not None:
                self.connection.close()
                self.connection = None
        except Exception as e:
            self.logger.error(
                "An error occurred while closing database connection: %s", e
            )
            raise DatabaseCloseConnectionException(
                "An error occurred while closing database connection"
            ) from e
