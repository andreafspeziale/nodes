from marshmallow import Schema, fields, validate


class ListNodesSchema:
    def __init__(
        self,
        valid_languages: list[str],
        default_page_number: int,
        default_page_size: int,
    ):
        self.schema = Schema.from_dict(
            {
                "language": fields.Str(
                    required=True, validate=lambda lan: lan in valid_languages
                ),
                "search_keyword": fields.Str(missing=""),
                "page_num": fields.Int(
                    missing=default_page_number, validate=lambda val: val >= 0
                ),
                "page_size": fields.Int(
                    missing=default_page_size,
                    validate=[validate.Range(min=0, max=1000)],
                ),
            }
        )

    def get_schema(self):
        return self.schema
