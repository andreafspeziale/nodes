# pylint: disable=R1732
import logging
import tempfile
import os
import pytest
from nodes.database import Database
from nodes.nodes_repository import (
    NodesRepository,
    ListNodesSearchParams,
)


@pytest.fixture(name="nodes_repository_fixture")
def create_nodes_repository():
    try:
        db_fd, db_path = tempfile.mkstemp()
        db = Database(logging, db_path)
        nodes_repository = NodesRepository(logging, db.get_connection())
        nodes_repository.migrate_or_seed(
            open(os.path.join(os.path.dirname(__file__), "sql/schema.sql"), mode="rb")
        )
        nodes_repository.migrate_or_seed(
            open(os.path.join(os.path.dirname(__file__), "sql/data.sql"), mode="rb")
        )
        yield nodes_repository
        db.close()
        os.close(db_fd)
        os.unlink(db_path)
    except Exception as e:
        logging.error("An error occurred while yield the nodes repository: %s", e)


def test_list_nodes_without_search_keyword(nodes_repository_fixture: NodesRepository):
    node_id = 7
    params: ListNodesSearchParams = {
        "language": "english",
        "search_keyword": "",
        "page_size": 100,
        "lower_bound": 0,
    }
    expected_nodes = [
        {"idNode": 8, "nodeName": "Italy", "count": 0},
        {"idNode": 9, "nodeName": "Europe", "count": 0},
        {"idNode": 11, "nodeName": "North America", "count": 0},
    ]
    nodes = nodes_repository_fixture.list_nodes(node_id, params)
    assert nodes == expected_nodes


def test_list_nodes_with_search_keyword(nodes_repository_fixture: NodesRepository):
    node_id = 5
    params: ListNodesSearchParams = {
        "language": "english",
        "search_keyword": "mar",
        "page_size": 100,
        "lower_bound": 0,
    }
    expected_nodes = [{"idNode": 1, "nodeName": "Marketing", "count": 0}]
    nodes = nodes_repository_fixture.list_nodes(node_id, params)
    assert nodes == expected_nodes


def test_list_nodes_with_count(nodes_repository_fixture: NodesRepository):
    node_id = 5
    params: ListNodesSearchParams = {
        "language": "english",
        "search_keyword": "sal",
        "page_size": 100,
        "lower_bound": 0,
    }
    expected_nodes = [{"idNode": 7, "nodeName": "Sales", "count": 3}]
    nodes = nodes_repository_fixture.list_nodes(node_id, params)
    assert nodes == expected_nodes


def test_list_nodes_with_page_num_and_page_size(
    nodes_repository_fixture: NodesRepository,
):
    node_id = 5
    params: ListNodesSearchParams = {
        "language": "english",
        "search_keyword": "",
        "page_size": 2,
        "lower_bound": 2,
    }
    expected_nodes = [
        {"idNode": 3, "nodeName": "Managers", "count": 0},
        {"idNode": 4, "nodeName": "Customer Account", "count": 0},
    ]
    nodes = nodes_repository_fixture.list_nodes(node_id, params)
    assert nodes == expected_nodes
