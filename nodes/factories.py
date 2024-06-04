from dataclasses import dataclass
from marshmallow import Schema, fields, validate


@dataclass
class ListNodesSchema:
    valid_languages: list[str]
    default_page_number: int
    default_page_size: int

    def build(self):
        return Schema.from_dict(
            {
                "language": fields.Str(
                    required=True, validate=lambda lan: lan in self.valid_languages
                ),
                "search_keyword": fields.Str(missing=""),
                "page_num": fields.Int(
                    missing=self.default_page_number, validate=lambda val: val >= 0
                ),
                "page_size": fields.Int(
                    missing=self.default_page_size,
                    validate=[validate.Range(min=0, max=1000)],
                ),
            }
        )
