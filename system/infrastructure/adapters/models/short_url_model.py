from datetime import datetime

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute

from system.infrastructure.adapters.models import BaseModel


class ShortUrlModel(BaseModel):
    original_url = UnicodeAttribute()
    short_url = UnicodeAttribute()
    created_at = UTCDateTimeAttribute(default_for_new=datetime.utcnow)
    updated_at = UTCDateTimeAttribute(default_for_new=datetime.utcnow)
    status = UnicodeAttribute()
