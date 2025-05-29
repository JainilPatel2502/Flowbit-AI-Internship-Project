from pydantic import BaseModel,Field,computed_field,EmailStr,FutureDate
from datetime import datetime
from typing import Annotated,Optional,Literal,List
class RequestSchema(BaseModel):
    items:Annotated[List[str],Field(description="Name of the list requested by the sender in the mail or json or pdf")]
    notes:Annotated[str,Field(description="Other notes  or requirments of the sender's request")]
    urgency:Annotated[Literal['low', 'medium', 'high', 'unspecified'],Field(description="How urgently the request must be resolved")]
    requested_date: Optional[datetime] = Field(
        None, description="Requested date of the request (or 'unspecified')"
    )
