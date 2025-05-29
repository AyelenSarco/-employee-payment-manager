from sqlalchemy import Table, Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from src.core.database import db

Rol_type = Enum (
    'Administrator',
    'Viewer',
    name = "user_rol_enum",
    metadata = db.metadata
)

rol_permission = Table (
    "roles_permissions",
    db.Model.metadata,
    Column("rol_id", Integer, ForeignKey("roles.id"), primary_key=True),
    Column("permisson_id", Integer, ForeignKey("permissions.id"), primary_key=True),
)

class Rol(db.Model):
    __tablename__ = "roles"

    id = Column (Integer, primary_key=True, autoincrement=True)
    name = Column(Rol_type, nullable=False)

    users = relationship("User", back_populates="rol")
    permissions = relationship("Permission", secondary="roles_permissions", back_populates="roles")

class Permission(db.Model):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    roles = relationship("Rol", secondary="roles_permissions", back_populates="permissions")
