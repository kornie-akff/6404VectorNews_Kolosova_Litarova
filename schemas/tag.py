from pydantic import BaseModel, Field

class TagBase(BaseModel):
    tag_name: str = Field(..., max_length=100)

class TagCreate(TagBase):
    pass

class TagOut(TagBase):
    tag_id: int
    
    class Config:
        from_attributes = True