# GA-GWO Timetabling — Backend API

Sistem penjadwalan sekolah otomatis menggunakan **Hybrid Genetic Algorithm (GA) & Grey Wolf Optimizer (GWO)**, dibangun dengan **FastAPI**.

## Struktur Folder

```
backend/
├── app/
│   ├── main.py                  # Entry point & app factory
│   ├── config.py                # Settings (env vars)
│   ├── dependencies.py          # Dependency injection container
│   │
│   ├── api/                     # Controller / Router layer
│   │   ├── router.py            # Aggregator semua sub‑router
│   │   └── v1/
│   │       ├── guru.py
│   │       ├── kelas.py
│   │       ├── mapel.py
│   │       ├── slot.py
│   │       ├── relasi_guru_mapel.py
│   │       ├── wali_kelas.py
│   │       └── schedule.py
│   │
│   ├── schemas/                 # Pydantic request/response models
│   │   ├── common.py
│   │   ├── guru.py
│   │   ├── kelas.py
│   │   ├── mapel.py
│   │   ├── slot.py
│   │   ├── relasi_guru_mapel.py
│   │   ├── wali_kelas.py
│   │   └── schedule.py
│   │
│   ├── services/                # Business logic layer
│   │   ├── guru_service.py
│   │   ├── kelas_service.py
│   │   ├── mapel_service.py
│   │   ├── slot_service.py
│   │   ├── relasi_guru_mapel_service.py
│   │   ├── wali_kelas_service.py
│   │   └── schedule_service.py
│   │
│   ├── repositories/            # Data access layer (CSV‑backed)
│   │   ├── base_repository.py   # Generic CRUD base class
│   │   ├── guru_repository.py
│   │   ├── kelas_repository.py
│   │   ├── mapel_repository.py
│   │   ├── slot_repository.py
│   │   ├── relasi_guru_mapel_repository.py
│   │   └── wali_kelas_repository.py
│   │
│   ├── core/                    # Cross‑cutting concerns
│   │   ├── exceptions.py        # Custom exceptions & handlers
│   │   └── logging.py           # Structured logging
│   │
│   └── algorithm/               # Scheduling algorithm
│       ├── dictionary.py        # Data dictionary (refactored)
│       ├── construct.py         # Population constructor
│       ├── evaluation.py        # Fitness evaluation
│       ├── ga.py                # Genetic Algorithm operators
│       ├── gwo.py               # Grey Wolf Optimizer
│       └── repair.py            # Constraint repair operator
│
├── data/csv/                    # Master data CSV files
├── tests/                       # Test suite
├── requirements.txt
├── .env                         # Environment config (local)
└── .env.example                 # Environment config template
```

## Arsitektur

```
Request → Router (API) → Service (Business Logic) → Repository (Data Access) → CSV/DB
                                      ↕
                              Algorithm Layer
```

| Layer          | Tanggung Jawab                                              |
| -------------- | ----------------------------------------------------------- |
| **Router**     | HTTP handling, validasi input (Pydantic), response envelope |
| **Service**    | Business rules, orkestrasi, validasi domain                 |
| **Repository** | CRUD ke data store (CSV). Ganti ke DB tanpa ubah service    |
| **Algorithm**  | Logika GA-GWO: construct, evaluate, optimize, repair        |
| **Core**       | Exception handling, logging                                 |

## Quick Start

```bash
cd backend

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

- **Swagger UI** : [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

## API Endpoints

### Data Master (CRUD)

| Method | Endpoint             | Deskripsi       |
| ------ | -------------------- | --------------- |
| GET    | `/api/v1/guru`       | Semua guru      |
| POST   | `/api/v1/guru`       | Tambah guru     |
| GET    | `/api/v1/guru/{id}`  | Detail guru     |
| PUT    | `/api/v1/guru/{id}`  | Update guru     |
| DELETE | `/api/v1/guru/{id}`  | Hapus guru      |
| _idem_ | `/api/v1/kelas`      | CRUD Kelas      |
| _idem_ | `/api/v1/mapel`      | CRUD Mapel      |
| _idem_ | `/api/v1/slot`       | CRUD Slot Waktu |
| _idem_ | `/api/v1/wali-kelas` | CRUD Wali Kelas |

### Relasi Guru-Mapel

| Method | Endpoint                                                  | Deskripsi        |
| ------ | --------------------------------------------------------- | ---------------- |
| GET    | `/api/v1/relasi-guru-mapel`                               | Semua relasi     |
| GET    | `/api/v1/relasi-guru-mapel/guru/{id}`                     | Relasi per guru  |
| GET    | `/api/v1/relasi-guru-mapel/mapel/{id}`                    | Relasi per mapel |
| POST   | `/api/v1/relasi-guru-mapel`                               | Tambah relasi    |
| DELETE | `/api/v1/relasi-guru-mapel?guru_id=&mapel_id=&tingkatan=` | Hapus relasi     |

### Penjadwalan

| Method | Endpoint                    | Deskripsi             |
| ------ | --------------------------- | --------------------- |
| POST   | `/api/v1/schedule/generate` | Mulai generate jadwal |
| GET    | `/api/v1/schedule/status`   | Cek status progress   |
| GET    | `/api/v1/schedule/latest`   | Ambil hasil terakhir  |
