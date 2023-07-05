from typing import Any, Dict, Type, Optional
from errors import HttpError
from pydantic import ValidationError
import pydantic

class CreateAdvert(pydantic.BaseModel):
    
    title: str
    username: str
    content: str
    

class PatchAdvert(pydantic.BaseModel):
    
    title: Optional[str]
    username: Optional[str]
    content: Optional[str]

SCHEMA_TYPE = Type[CreateAdvert] | Type[PatchAdvert]


def validate(schema: SCHEMA_TYPE, data: Dict[str, Any], exclude_none: bool = True) -> dict:
    try:
        validated = schema(**data).dict(exclude_none=exclude_none)
    except ValidationError as er:
        raise HttpError(400, er.errors())
    return validated