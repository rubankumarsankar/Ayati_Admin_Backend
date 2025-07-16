from pydantic import BaseModel, EmailStr
from typing import Optional

# ✅ ROLE SCHEMAS
class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleOut(RoleBase):
    id: int

    class Config:
        from_attributes = True


# ✅ ADMIN SCHEMAS
class AdminBase(BaseModel):
    name: str
    email: EmailStr

class AdminCreate(AdminBase):
    password: str
    role_id: int  # ✅ Use role_id instead of role name

class AdminOut(AdminBase):
    id: int
    is_active: bool
    role_rel: RoleOut  # ✅ Include Role details (id, name, description)

    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


# ✅ EMPLOYEE SCHEMAS
class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    department: str
    role_id: Optional[int] = None  # ✅ Linked to Role table

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeOut(EmployeeBase):
    id: int
    is_active: bool
    role_rel: Optional[RoleOut] = None  # ✅ Return role details if available

    class Config:
        from_attributes = True
