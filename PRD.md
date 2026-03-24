# Product Requirement Document (PRD) - GA-GWO Timetabling

## 1. Pendahuluan
Dokumen ini menguraikan persyaratan fungsional dan teknis untuk antarmuka pengguna (UI) dan antarmuka pemrograman aplikasi (API) dari sistem penjadwalan sekolah menggunakan algoritma Hybrid Genetic Algorithm (GA) dan Grey Wolf Optimizer (GWO).

### 1.1 Tujuan
Membangun sistem yang dapat membantu administrator sekolah dalam menyusun jadwal pelajaran secara otomatis dengan mempertimbangkan berbagai batasan (constraints) dan mengoptimalkan penggunaan sumber daya (guru, kelas, waktu).

### 1.2 Target Pengguna
- **Administrator Sekolah**: Mengelola data master dan mengatur parameter algoritma.
- **Akademik**: Meninjau dan mempublikasikan jadwal yang dihasilkan.

---

## 2. Persyaratan UI (User Interface)

Desain UI harus modern, responsif, dan mudah digunakan (User-Friendly). Tema yang disarankan adalah **Sleek Dark Mode** atau **Clean Professional Light Mode**.

### 2.1 Halaman Dashboard
- Ringkasan statistik (Jumlah Guru, Kelas, Mapel, Slot Waktu).
- Status penjadwalan terakhir.
- Pintasan (shortcuts) untuk melakukan aksi cepat.

### 2.2 Manajemen Data Master (CRUD)
Setiap data master memerlukan halaman tabel dengan fitur Tambah, Edit, Hapus, dan Pencarian:
- **Data Guru**: Nama, NIP, ketersediaan waktu.
- **Data Kelas**: Nama kelas, tingkat, kapasitas.
- **Data Mata Pelajaran**: Nama mapel, kategori, beban jam.
- **Data Slot Waktu**: Hari, jam ke-, durasi.
- **Relasi Guru-Mapel**: Menghubungkan guru dengan mapel yang diampu dan kelas tertentu.
- **Wali Kelas**: Penugasan wali kelas untuk setiap kelas.

### 2.3 Konfigurasi & Eksekusi Algoritma
- **Input Parameter GA**:
  - Ukuran Populasi (Population Size).
  - Probabilitas Crossover & Mutasi.
- **Input Parameter GWO**:
  - Jumlah Wolf (Agen).
  - Maksimum Iterasi.
- **Tombol "Generate Jadwal"**: Menjalankan algoritma di backend.
- **Progress Bar**: Menampilkan status iterasi atau kemajuan algoritma secara real-time.

### 2.4 Visualisasi & Hasil Jadwal
- **Tampilan Grid Jadwal**: Menampilkan hasil jadwal dalam format tabel harian (Senin - Jumat) per kelas atau per guru.
- **Highlight Bentrok**: Menandai (marking) jika masih ada jadwal yang kurang optimal atau melanggar batasan ringan (soft constraints).
- **Export Data**: Fitur untuk mengekspor jadwal ke format PDF atau Excel (CSV).

---

## 3. Persyaratan API (Application Programming Interface)

API akan dibangun menggunakan **FastAPI (Python)**.

### 3.1 Endpoint Data Master (RESTful)
- `GET /api/guru`: Mengambil semua data guru.
- `POST /api/guru`: Menambah data guru baru.
- `PUT /api/guru/{id}`: Memperbarui data guru.
- `DELETE /api/guru/{id}`: Menghapus data guru.
- *(Berlaku juga untuk `/api/kelas`, `/api/mapel`, `/api/slot`, dll.)*

### 3.2 Endpoint Algoritma (Scheduling)
- `POST /api/schedule/generate`: Menjalankan proses optimasi GA-GWO.
  - Body: `{ pop_size: int, iterations: int, ... }`
- `GET /api/schedule/status`: Mendapatkan status proses yang sedang berjalan (Running/Success/Failed).
- `GET /api/schedule/latest`: Mengambil hasil penjadwalan terakhir yang tersimpan.

### 3.3 Endpoint Analisis (Evaluation)
- `GET /api/schedule/fitness`: Melihat nilai fitness dari jadwal yang dihasilkan.
- `GET /api/schedule/conflicts`: Mendapatkan rincian bentrok (jika ada) demi perbaikan manual.

---

## 4. Alur Kerja Sistem (Workflow)
1. User mengunggah atau memasukkan data master melalui UI.
2. User mengatur parameter algoritma di halaman konfigurasi.
3. User menekan tombol "Generate".
4. UI memanggil API `/generate`, dan memantau progress via `/status`.
5. Setelah selesai, API mengembalikan hasil jadwal dalam format JSON.
6. UI menampilkan hasil jadwal dalam grid yang mudah dibaca.
7. User dapat mengekspor atau menyimpan hasil jadwal tersebut.

---

## 5. Teknologi yang Digunakan
- **Frontend**: React.js atau Next.js dengan Tailwind CSS.
- **Backend**: FastAPI (Python).
- **Database**: PostgreSQL (untuk menyimpan data master dan histori jadwal) atau CSV (untuk skenario sederhana).
- **Algorithm**: Hybrid GA-GWO (Genetic Algorithm & Grey Wolf Optimizer).
