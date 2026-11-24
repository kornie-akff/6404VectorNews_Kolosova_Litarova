from pydantic import BaseModel, Field

class RoleBase(BaseModel):
    role_name: str = Field(..., max_length=50)

class RoleCreate(RoleBase):
    pass

class RoleOut(RoleBase):
    role_id: int
    class Config:
        from_attributes = True