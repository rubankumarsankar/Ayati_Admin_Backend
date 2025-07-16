from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
from app.routes.admins import super_admin_only

router = APIRouter(prefix="/roles", tags=["Roles"])

# ✅ Create Role (Super Admin Only)
@router.post("/", response_model=schemas.RoleOut, status_code=status.HTTP_201_CREATED)
def create_role(
    role: schemas.RoleCreate,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(super_admin_only)
):
    existing = db.query(models.Role).filter(models.Role.name == role.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Role already exists")

    new_role = models.Role(**role.dict())
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

# ✅ List Roles
@router.get("/", response_model=List[schemas.RoleOut])
def list_roles(db: Session = Depends(get_db)):
    return db.query(models.Role).all()

# ✅ Update Role (Super Admin Only)
@router.put("/{role_id}", response_model=schemas.RoleOut)
def update_role(
    role_id: int,
    role: schemas.RoleCreate,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(super_admin_only)
):
    db_role = db.query(models.Role).get(role_id)
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")

    db_role.name = role.name
    db_role.description = role.description
    db.commit()
    db.refresh(db_role)
    return db_role

# ✅ Delete Role (Super Admin Only)
@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(super_admin_only)
):
    db_role = db.query(models.Role).get(role_id)
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")

    db.delete(db_role)
    db.commit()
    return {"message": "Role deleted successfully"}
