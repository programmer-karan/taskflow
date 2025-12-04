from datetime import datetime
from pydantic import BaseModel, ConfigDict

class TaskCreate(BaseModel):
    title: str
    # The None here makes the field optional in JSON.
    description: str | None = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    created_at: datetime
    owner_id: int
    
    # This tells Pydantic "It's okay to read data from a Class object"
    model_config = ConfigDict(from_attributes=True)