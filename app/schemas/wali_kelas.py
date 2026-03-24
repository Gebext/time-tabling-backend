from pydantic import BaseModel, Field

class WaliKelasBase(BaseModel):

    guru_id: int = Field(..., ge=1)

    kelas_id: int = Field(..., ge=1)

class WaliKelasCreate(WaliKelasBase):

    pass

class WaliKelasUpdate(BaseModel):

    guru_id: int | None = Field(None, ge=1)

    kelas_id: int | None = Field(None, ge=1)

class WaliKelasResponse(WaliKelasBase):

    model_config = {"from_attributes": True}
