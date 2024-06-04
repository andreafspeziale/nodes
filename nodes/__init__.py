import os
import sys
from typing import TypedDict, cast
from flask import Flask
from .database import Database
from .nodes_repository import NodesRepository
from .nodes_service import NodesService
from .nodes_routes import NodesRoutes
from .factories import ListNodesSchema


class Config(TypedDict):
    DATABASE: str
    VALID_LANGUAGES: list[str]
    DEFAULT_PAGE_NUMBER: int
    DEFAULT_PAGE_SIZE: int


def create_app(test_config: dict[str, str] | None = None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "nodes.sqlite"),
        VALID_LANGUAGES=["italian", "english"],
        DEFAULT_PAGE_NUMBER=0,
        DEFAULT_PAGE_SIZE=100,
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    config: Config = cast(Config, app.config)

    try:
        db = Database(app.logger, config["DATABASE"])
    except Exception as e:
        app.logger.error("An error occurred while creating the nodes app: %s", e)
        sys.exit(1)

    try:
        nodes_repository = NodesRepository(app.logger, db.get_connection())

        migration = app.open_resource("sql/schema.sql")
        seed = app.open_resource("sql/data.sql")

        nodes_repository.migrate_or_seed(migration)
        nodes_repository.migrate_or_seed(seed)

        nodes_service = NodesService(app.logger, nodes_repository)

        list_nodes_schema = ListNodesSchema(
            app.config["VALID_LANGUAGES"],
            app.config["DEFAULT_PAGE_NUMBER"],
            app.config["DEFAULT_PAGE_SIZE"],
        )

        nodes_routes = NodesRoutes(app.logger, list_nodes_schema, nodes_service)
        app.register_blueprint(nodes_routes.get_blueprint())
    except Exception as e:
        app.logger.error("An error occurred while creating the nodes app: %s", e)
        db.close()
        sys.exit(1)

    return app
