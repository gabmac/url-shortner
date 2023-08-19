from typing import Any

from pynamodb.attributes import Attribute
from pynamodb.constants import STRING
from ulid import ULID


class DecimalAttribute(Attribute[Any]):
    attr_type = STRING

    def __init__(self, context: Any = None, **kwargs: Any):
        super().__init__(**kwargs)
        self.context = context

    def serialize(self, value: ULID) -> str:
        # decimal.Decimal -> str
        return str(self.context.create_decimal(str(value)))

    def deserialize(self, value: str) -> ULID:
        # str -> decimal.Decimal
        return self.context.create_decimal(value)
