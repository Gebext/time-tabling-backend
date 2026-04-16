from pydantic import BaseModel, Field

class ScheduleRequest(BaseModel):

    population_size: int = Field(default=50, ge=5, le=500, examples=[50])

    max_iterations: int = Field(default=500, ge=10, le=10000, examples=[500])

    tournament_size: int = Field(default=15, ge=3, le=100, examples=[15])

    gwo_interval: int = Field(

        default=20, ge=5, le=100, examples=[20],

        description="Setiap berapa generasi GA, fase GWO dijalankan",

    )

    gwo_iterations: int = Field(

        default=20, ge=1, le=100, examples=[20],

        description="Jumlah iterasi GWO per fase",

    )

class ScheduleStatusResponse(BaseModel):

    status: str = Field(..., examples=["running"], description="idle | running | completed | failed | cancelled")

    progress: float = Field(default=0.0, ge=0.0, le=100.0, description="Persentase progress")

    best_fitness: float | None = Field(default=None, description="Nilai fitness terbaik saat ini")

    message: str = ""

class ScheduleSlotDetail(BaseModel):

    slot_id: int

    hari: str

    jam_mulai: str

    jam_selesai: str

    mapel_id: int

    mapel_nama: str

    guru_id: int

    guru_nama: str

class ScheduleKelasResult(BaseModel):

    kelas_id: int

    kelas_nama: str

    jadwal: list[ScheduleSlotDetail] = []

class ScheduleResult(BaseModel):

    fitness: float

    total_conflicts: int

    detail_per_kelas: list[ScheduleKelasResult] = []

class FitnessDetail(BaseModel):

    guru_bentrok: float = 0.0

    distribusi_mapel: float = 0.0

    konsistensi_guru_mapel: float = 0.0

    durasi_guru: float = 0.0

    waktu_mgmp: float = 0.0

    mapel_siang: float = 0.0

    cek_wali_kelas: float = 0.0

    total: float = 0.0

class ScheduleSummary(BaseModel):

    schedule_id: int

    filename: str

    fitness: float

    total_conflicts: int

    created_at: str

class ScheduleRowDetail(BaseModel):

    kelas_id: int

    kelas_nama: str

    slot_id: int

    hari: str

    jam_mulai: str

    jam_selesai: str

    mapel_id: int

    mapel_nama: str

    guru_id: int

    guru_nama: str

class ScheduleDetailResponse(BaseModel):

    summary: ScheduleSummary

    data: list[ScheduleRowDetail] = []
