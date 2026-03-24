"""
Pydantic schemas for Mapel (Subject) entity.
"""

from pydantic import BaseModel, Field


HARI_VALID = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]


class MapelBase(BaseModel):
    kode_mapel: str = Field(..., min_length=1, max_length=5, examples=["A"])
    nama_mapel: str = Field(..., min_length=1, max_length=200, examples=["MATEMATIKA"])
    mgmp: str = Field(..., examples=["Senin"], description="Hari MGMP (Senin-Jumat)")
    jam_per_minggu: int = Field(..., ge=1, le=10, examples=[4])


class MapelCreate(MapelBase):
    """Schema untuk menambah mapel baru."""
    pass


class MapelUpdate(BaseModel):
    """Schema untuk update data mapel. Semua field opsional."""
    kode_mapel: str | None = Field(None, min_length=1, max_length=5)
    nama_mapel: str | None = Field(None, min_length=1, max_length=200)
    mgmp: str | None = Field(None)
    jam_per_minggu: int | None = Field(None, ge=1, le=10)


class MapelResponse(MapelBase):
    """Schema response mapel."""
    mapel_id: int

    model_config = {"from_attributes": True}
