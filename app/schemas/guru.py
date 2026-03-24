"""
Pydantic schemas for Guru (Teacher) entity.
"""

from pydantic import BaseModel, Field


class GuruBase(BaseModel):
    nama_guru: str = Field(..., min_length=1, max_length=200, examples=["Budi Santoso, S.Pd."])


class GuruCreate(GuruBase):
    """Schema untuk menambah guru baru."""
    pass


class GuruUpdate(BaseModel):
    """Schema untuk update data guru. Semua field opsional."""
    nama_guru: str | None = Field(None, min_length=1, max_length=200)


class GuruResponse(GuruBase):
    """Schema response guru."""
    guru_id: int

    model_config = {"from_attributes": True}
