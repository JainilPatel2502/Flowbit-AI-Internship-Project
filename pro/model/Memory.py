from pydantic import BaseModel, EmailStr, Field,computed_field
from typing import List, Union, Optional
import time
class MemoryEntry(BaseModel):
    input: str
    output: Union[str, dict]
    @computed_field
    @property
    def timestamp(self) -> float:
        return time.time()


class EntityMemory(BaseModel):
    entity: EmailStr
    history: List[MemoryEntry]
