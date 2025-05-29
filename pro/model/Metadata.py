from pydantic import BaseModel,Field,computed_field,EmailStr
from typing import Annotated,Optional,Literal,List
import time
class MetaDataSchema(BaseModel):
    conversation_id:Annotated[Optional[str],Field(description="Referring to the older email or request")]
    format:Annotated[Literal['json','email','pdf'],Field(description='The source of the request')]
    @computed_field
    @property
    def recived_at(self) -> float:
        return time.time()
    
