from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List
from app import models, schemas
from app.database import get_db
from app.routes.admins import get_current_admin

router = APIRouter(prefix="/employees", tags=["Employees"])


# ✅ Create Employee
@router.post("/", response_model=schemas.EmployeeOut, status_code=status.HTTP_201_CREATED)
def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    admin: models.Admin = Depends(get_current_admin)
):
    # Check if email already exists
    existing_employee = db.query(models.Employee).filter(models.Employee.email == employee.email).first()
    if existing_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new employee
    new_employee = models.Employee(**employee.dict(), admin_id=admin.id)
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


# ✅ List Employees (with search + pagination)
@router.get("/", response_model=List[schemas.EmployeeOut])
def list_employees(
    skip: int = 0,
    limit: int = 10,
    search: str = "",
    db: Session = Depends(get_db),
    admin: models.Admin = Depends(get_current_admin)
):
    query = db.query(models.Employee)

    # ✅ Proper search using or_
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                models.Employee.name.ilike(search_pattern),        # case-insensitive search
                models.Employee.department.ilike(search_pattern),
                models.Employee.role.ilike(search_pattern)
            )
        )

    employees = query.offset(skip).limit(limit).all()
    return employees
