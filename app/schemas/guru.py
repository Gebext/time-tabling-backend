from pydantic import BaseModel, Field

class GuruBase(BaseModel):
    kode_guru: str = Field("G-?", min_length=1, max_length=50, examples=["G01"])
    nama_guru: str = Field(..., min_length=1, max_length=200, examples=["Budi Santoso, S.Pd."])

class GuruCreate(GuruBase):
    pass

class GuruUpdate(BaseModel):
    kode_guru: str | None = Field(None, min_length=1, max_length=50)
    nama_guru: str | None = Field(None, min_length=1, max_length=200)

class GuruResponse(GuruBase):
    guru_id: int
    model_config = {"from_attributes": True}
