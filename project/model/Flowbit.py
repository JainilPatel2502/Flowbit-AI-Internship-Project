from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Optional,Literal,List
from project.model.Customer import CutomerSchema
from project.model.Metadata import MetaDataSchema
from project.model.Request import RequestSchema
from uuid import uuid4
class FlowbitSchema(BaseModel):
    source_type:Annotated[Literal['json','email','pdf'],Field(description='This will tell about the source of the request')]
    intent:Annotated[Literal['RFQ','Invoice','Complaint'],Field(description="This will tell the intent of the request")]
    tone:Annotated[Literal['escalation','polite','threatening'],Field(description="The tone in which the data is written")]
    total:Annotated[Optional[int],Field(description="give the total amout of the qoutation or invoice")]
    # policy:Annotated[Optional[Literal["GDPR","FDA"]],Field(description="if the policy mentions ")] 
    customer:CutomerSchema
    request:RequestSchema
    metadata:MetaDataSchema