from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app import models, schemas, auth
from app.database import get_db

router = APIRouter(prefix="/admins", tags=["Admins"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admins/login")


# ✅ GET CURRENT ADMIN
def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = auth.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Not authenticated")

    admin = db.query(models.Admin).filter(models.Admin.email == payload.get("sub")).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    if not admin.is_active:
        raise HTTPException(status_code=403, detail="Account is deactivated")

    return admin


# ✅ SUPER ADMIN ONLY
def super_admin_only(current_admin: models.Admin = Depends(get_current_admin)):
    if current_admin.role_rel.name != "super_admin":
        raise HTTPException(status_code=403, detail="Only super admins can perform this action")
    return current_admin


# ✅ REGISTER ADMIN (First Super Admin Open, Others Restricted)
@router.post("/register", response_model=schemas.AdminOut, status_code=status.HTTP_201_CREATED)
def register_admin(
    admin: schemas.AdminCreate,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(get_current_admin)  # Will be bypassed for first admin
):
    # ✅ If NO admin exists, allow first super admin creation (no token required)
    if db.query(models.Admin).count() == 0:
        # Ensure super_admin role exists
        role = db.query(models.Role).filter(models.Role.name == "super_admin").first()
        if not role:
            role = models.Role(name="super_admin", description="Full system access")
            db.add(role)
            db.commit()
            db.refresh(role)

        hashed = auth.hash_password(admin.password)
        new_admin = models.Admin(
            name=admin.name,
            email=admin.email,
            password=hashed,
            role_id=role.id,
            is_active=True
        )
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        return new_admin

    # ✅ Normal flow: only super admins can create admins
    if current_admin.role_rel.name != "super_admin":
        raise HTTPException(status_code=403, detail="Only super admins can register new admins")

    if db.query(models.Admin).filter(models.Admin.email == admin.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    role = db.query(models.Role).filter(models.Role.id == admin.role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    hashed = auth.hash_password(admin.password)
    new_admin = models.Admin(
        name=admin.name,
        email=admin.email,
        password=hashed,
        role_id=role.id,
        is_active=True
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin


# ✅ LOGIN ADMIN
@router.post("/login")
def login_admin(login: schemas.LoginSchema, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.email == login.email).first()
    if not admin or not auth.verify_password(login.password, admin.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not admin.is_active:
        raise HTTPException(status_code=403, detail="Account is deactivated")

    token = auth.create_access_token({"sub": admin.email, "role": admin.role_rel.name})
    return {"access_token": token, "token_type": "bearer"}


# ✅ LIST ADMINS (Super Admin Only)
@router.get("/", response_model=list[schemas.AdminOut])
def list_admins(db: Session = Depends(get_db), current_admin: models.Admin = Depends(super_admin_only)):
    return db.query(models.Admin).all()


# ✅ DEACTIVATE ADMIN (Super Admin Only)
@router.put("/deactivate/{admin_id}", status_code=status.HTTP_200_OK)
def deactivate_admin(
    admin_id: int,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(super_admin_only)
):
    admin = db.get(models.Admin, admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    if not admin.is_active:
        raise HTTPException(status_code=400, detail="Admin is already deactivated")

    admin.is_active = False
    db.commit()
    return {"message": f"Admin {admin.name} deactivated successfully"}
