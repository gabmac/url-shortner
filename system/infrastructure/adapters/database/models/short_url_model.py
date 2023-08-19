from datetime import datetime
from typing import Any

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute

from system.infrastructure.adapters.database.models.base_model import BaseModel


class ShortUrlModel(BaseModel):
    redirect_url = UnicodeAttribute()
    short_url = UnicodeAttribute()
    created_at = UTCDateTimeAttribute(default_for_new=datetime.utcnow)
    updated_at = UTCDateTimeAttribute(default_for_new=datetime.utcnow)
    status = UnicodeAttribute()

    def __init__(self, populate_all_fields: bool = False, **attributes: Any) -> None:
        if populate_all_fields:
            attributes["pk"] = "ROUTE"
            attributes["sk"] = attributes["short_url"]

        super().__init__(**attributes)
