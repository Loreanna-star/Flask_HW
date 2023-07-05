from flask import Flask

from typing import Optional
import pydantic

class CreateAdvert(pydantic.BaseModel):
    
    title: str
    username: str
    content: str
    

class PatchAdvert(pydantic.BaseModel):
    
    title: Optional[str]
    username: Optional[str]
    content: Optional[str]
