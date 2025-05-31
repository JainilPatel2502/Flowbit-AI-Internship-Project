from pydantic import BaseModel,Field,computed_field,EmailStr
from typing import Annotated,Optional,Literal,List
class CutomerSchema(BaseModel):
    name:Annotated[str,Field(description="Name of the sender")]
    email:Annotated[str,Field(description='Email of the sender')]
    organization:Annotated[Optional[str],Field(description="Name of the organization of the sender")]
