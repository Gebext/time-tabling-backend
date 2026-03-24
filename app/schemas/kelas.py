"""
Pydantic schemas for Kelas (Class) entity.
"""

from pydantic import BaseModel, Field


class KelasBase(BaseModel):
    nama_kelas: str = Field(..., min_length=1, max_length=10, examples=["7A"])
    tingkatan: int = Field(..., ge=7, le=12, examples=[7])


class KelasCreate(KelasBase):
    """Schema untuk menambah kelas baru."""
    pass


class KelasUpdate(BaseModel):
    """Schema untuk update data kelas. Semua field opsional."""
    nama_kelas: str | None = Field(None, min_length=1, max_length=10)
    tingkatan: int | None = Field(None, ge=7, le=12)


class KelasResponse(KelasBase):
    """Schema response kelas."""
    kelas_id: int

    model_config = {"from_attributes": True}
