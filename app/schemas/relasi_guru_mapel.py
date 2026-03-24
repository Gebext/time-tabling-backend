from pydantic import BaseModel, Field

class RelasiGuruMapelBase(BaseModel):

    guru_id: int = Field(..., ge=1)

    mapel_id: int = Field(..., ge=1)

    tingkatan: int = Field(..., ge=7, le=12, examples=[7])

    durasi: int = Field(..., ge=1, examples=[24], description="Durasi jam per semester")

class RelasiGuruMapelCreate(RelasiGuruMapelBase):

    pass

class RelasiGuruMapelUpdate(BaseModel):

    guru_id: int | None = Field(None, ge=1)

    mapel_id: int | None = Field(None, ge=1)

    tingkatan: int | None = Field(None, ge=7, le=12)

    durasi: int | None = Field(None, ge=1)

class RelasiGuruMapelResponse(RelasiGuruMapelBase):

    model_config = {"from_attributes": True}
