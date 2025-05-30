from pydantic import BaseModel, Field , EmailStr
from typing import Literal,Annotated
class ClassifySchema(BaseModel):
    type:Annotated[Literal['email','json'],Field(description="this will classify the input if the input is a json then json and if the email then it will be an email")]
    data:Annotated[str,Field(description="pass the input data further for the extraction if inpur is json then send the json and if the input is email then again sent the email as it is send the input as it is" )]
    email:Annotated[str,Field(description="Extract the email adress from the mail or json")]