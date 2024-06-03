from typing import TypedDict
from logging import Logger
from .nodes_repository import NodesRepository


class ListNodesParams(TypedDict):
    language: str
    search_keyword: str
    page_size: int
    lower_bound: int


class ListNodesServiceException(Exception):
    pass


class NodesService:
    def __init__(self, logger: Logger, nodes_repository: NodesRepository):
        self.logger = logger
        self.nodes_repository = nodes_repository

    def list_nodes(self, node_id: int, params: ListNodesParams):
        self.logger.debug("Retrieving nodes list...")
        try:
            nodes = self.nodes_repository.list_nodes(node_id, params)
        except Exception as e:
            self.logger.error("An error occurred while retrieving nodes list: %s", e)
            raise ListNodesServiceException(e)
        else:
            return nodes
