from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)  # e.g., "super_admin", "manager", "staff"
    description = Column(String(255), nullable=True)

    # Relationships
    employees = relationship("Employee", back_populates="role_rel")
    admins = relationship("Admin", back_populates="role_rel")


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)  # ✅ Linked to Role table

    # Relationships
    role_rel = relationship("Role", back_populates="admins")
    employees = relationship("Employee", back_populates="admin")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20))
    department = Column(String(100))
    is_active = Column(Boolean, default=True)

    admin_id = Column(Integer, ForeignKey("admins.id"))
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)  # ✅ Linked to Role table

    # Relationships
    admin = relationship("Admin", back_populates="employees")
    role_rel = relationship("Role", back_populates="employees")
