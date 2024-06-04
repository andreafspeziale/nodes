from typing import TypedDict, cast, IO
from logging import Logger
from sqlite3 import Connection


class Node(TypedDict):
    count: int
    idNode: int
    nodeName: str


class ListNodesSearchParams(TypedDict):
    language: str
    search_keyword: str
    page_size: int
    lower_bound: int


class ListNodesRepositoryException(Exception):
    pass


class MigrateOrSeedRepositoryException(Exception):
    pass


class NodesRepository:
    def __init__(self, logger: Logger, connection: Connection):
        self.logger = logger
        self.connection = connection

    def migrate_or_seed(self, resources: IO):
        self.logger.debug("Running database migration etc...")
        try:
            with resources as f:
                self.connection.executescript(f.read().decode("utf8"))
        except Exception as e:
            self.logger.error("Error while running database migration etc.: %s", e)
            raise MigrateOrSeedRepositoryException(
                "Error while running database migration etc."
            ) from e

    def list_nodes(self, node_id: int, params: ListNodesSearchParams):
        self.logger.debug("Retrieving nodes list...")
        try:
            query = """ WITH node AS (
                SELECT *, (iRight - iLeft - 1) / 2 as count FROM node_tree
                JOIN node_tree_names ON idNode=node_tree_idNode
                WHERE iLeft > (SELECT iLeft from node_tree WHERE idNode=:node_id)
                    AND iRight < (SELECT iRight from node_tree WHERE idNode=:node_id)
                    AND language=:language
                    AND nodeName LIKE :search_keyword
                LIMIT :lower_bound, :page_size
                )
                SELECT idNode, nodeName, count FROM node;
            """

            p = {
                "node_id": node_id,
                "language": params["language"],
                "search_keyword": f"%{params['search_keyword']}%",
                "lower_bound": params["lower_bound"],
                "page_size": params["page_size"],
            }

            data = self.connection.execute(query, p).fetchall()
            nodes = cast(list[Node], [dict(node) for node in data])
        except Exception as e:
            self.logger.error(
                "An error occurred while retrieving nodes list from database: %s", e
            )
            raise ListNodesRepositoryException(
                "An error occurred while retrieving nodes list from database"
            ) from e
        return nodes
