from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Optional,Literal,List
from pro.model.Customer import CutomerSchema
from pro.model.Metadata import MetaDataSchema
from pro.model.Request import RequestSchema
from uuid import uuid4
class FlowbitSchema(BaseModel):
    id : Annotated[str, Field(description="This is a unique id for the CRM")] = Field(default_factory=lambda: str(uuid4()))
    source_type:Annotated[Literal['json','email','pdf'],Field(description='This will tell about the source of the request')]
    intent:Annotated[Literal['RFQ','Invoice','Complaint'],Field(description="This will tell the intent of the request")]
    customer:CutomerSchema
    request:RequestSchema
    metadata:MetaDataSchema