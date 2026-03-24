"""
Pydantic schemas for Relasi Guru-Mapel (Teacher-Subject Relation) entity.
"""

from pydantic import BaseModel, Field


class RelasiGuruMapelBase(BaseModel):
    guru_id: int = Field(..., ge=1)
    mapel_id: int = Field(..., ge=1)
    tingkatan: int = Field(..., ge=7, le=12, examples=[7])
    durasi: int = Field(..., ge=1, examples=[24], description="Durasi jam per semester")


class RelasiGuruMapelCreate(RelasiGuruMapelBase):
    """Schema untuk menambah relasi guru-mapel baru."""
    pass


class RelasiGuruMapelUpdate(BaseModel):
    """Schema untuk update relasi guru-mapel."""
    guru_id: int | None = Field(None, ge=1)
    mapel_id: int | None = Field(None, ge=1)
    tingkatan: int | None = Field(None, ge=7, le=12)
    durasi: int | None = Field(None, ge=1)


class RelasiGuruMapelResponse(RelasiGuruMapelBase):
    """Schema response relasi guru-mapel."""

    model_config = {"from_attributes": True}
