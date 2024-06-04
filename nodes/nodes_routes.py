from typing import TypedDict
from flask import Blueprint, jsonify
from webargs.flaskparser import use_args
from .factories import ListNodesSchema
from .nodes_service import NodesService, ListNodesParams


class ListNodesArgs(TypedDict):
    language: str
    search_keyword: str
    page_num: int
    page_size: int


class NodesRoutes:
    def __init__(
        self, logger, list_nodes_schema: ListNodesSchema, nodes_service: NodesService
    ):
        self.logger = logger
        self.list_nodes_schema = list_nodes_schema.build()
        self.nodes_service = nodes_service
        self.blueprint = Blueprint("my_routes", __name__)
        self.register_routes()

    def get_blueprint(self):
        return self.blueprint

    def register_routes(self):
        @self.blueprint.route("/api/nodes/<int:node_id>/children")
        @use_args(self.list_nodes_schema, location="querystring")
        def nodes(args: ListNodesArgs, node_id: int):
            try:
                self.logger.debug("Retrieving nodes list...")
                params: ListNodesParams = {
                    "language": args["language"],
                    "search_keyword": args["search_keyword"],
                    "page_size": args["page_size"],
                    "lower_bound": args["page_num"] * args["page_size"],
                }
                result = self.nodes_service.list_nodes(node_id, params)
                code = 200
                response = {"nodes": result}
            except Exception as e:
                self.logger.error(
                    "An error occurred while retrieving nodes list: %s", e
                )
                code = 500
                response = {"error": "Internal server error"}
            return jsonify(response), code

        @self.blueprint.errorhandler(422)
        @self.blueprint.errorhandler(400)
        def handle_error(err):
            headers = err.data.get("headers", None)
            messages = err.data.get("messages", ["Invalid request."])
            if headers:
                return jsonify({"errors": messages}), err.code, headers
            return jsonify({"errors": messages}), err.code
