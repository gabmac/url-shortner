import json
from typing import Any, Dict

from pydantic import BaseModel


class BaseEntity(BaseModel):
    class Config:
        allow_population_by_field_name = True
        orm_mode = True
        use_enum_values = True
        arbitrary_types_allowed = True
        validate_assignment = True
        from_attributes = True

    def to_jsonable_dict(
        self,
        **kwargs: Dict[Any, Any],
    ) -> Dict[Any, Any]:
        return json.loads(self.model_dump_json(**kwargs))  # type: ignore[arg-type]
