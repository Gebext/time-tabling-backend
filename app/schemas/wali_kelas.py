"""
Pydantic schemas for Wali Kelas (Homeroom Teacher) entity.
"""

from pydantic import BaseModel, Field


class WaliKelasBase(BaseModel):
    guru_id: int = Field(..., ge=1)
    kelas_id: int = Field(..., ge=1)


class WaliKelasCreate(WaliKelasBase):
    """Schema untuk menambah wali kelas baru."""
    pass


class WaliKelasUpdate(BaseModel):
    """Schema untuk update wali kelas."""
    guru_id: int | None = Field(None, ge=1)
    kelas_id: int | None = Field(None, ge=1)


class WaliKelasResponse(WaliKelasBase):
    """Schema response wali kelas."""

    model_config = {"from_attributes": True}
