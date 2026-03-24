"""
Pydantic schemas for Slot (Time Slot) entity.
"""

from pydantic import BaseModel, Field


class SlotBase(BaseModel):
    hari: str = Field(..., examples=["Senin"], description="Hari (Senin-Jumat)")
    jam_mulai: str = Field(..., examples=["07:40"], description="Format HH:MM")
    jam_selesai: str = Field(..., examples=["08:20"], description="Format HH:MM")
    jenis_slot: str = Field(default="pelajaran", examples=["pelajaran"])


class SlotCreate(SlotBase):
    """Schema untuk menambah slot baru."""
    pass


class SlotUpdate(BaseModel):
    """Schema untuk update data slot. Semua field opsional."""
    hari: str | None = Field(None)
    jam_mulai: str | None = Field(None)
    jam_selesai: str | None = Field(None)
    jenis_slot: str | None = Field(None)


class SlotResponse(SlotBase):
    """Schema response slot."""
    slot_id: int

    model_config = {"from_attributes": True}
