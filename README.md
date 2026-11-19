# CyberSOC API v1.0.0

REST API MVP untuk **Security Event Monitoring & Incident Response** menggunakan Python Flask, Flask-SQLAlchemy ORM, SQLite, dan pola MVC. Seluruh data demonstrasi bersifat sintetis.

## 1. Lima Tabel Utama

1. `log_sources`: sumber log (server, firewall, endpoint).
2. `security_events`: event keamanan yang diterima dari sumber log.
3. `detection_rules`: aturan identifikasi event mencurigakan.
4. `alerts`: peringatan yang menghubungkan event dengan aturan deteksi.
5. `investigations`: catatan analisis dan tindak lanjut alert.

ERD tersedia di `docs/erd.md`.

## 2. Fitur

- Registrasi, pembacaan, pembaruan, dan penghapusan sumber log.
- Ingest dan pencarian event keamanan.
- Pengelolaan aturan deteksi.
- Pembuatan dan pembaruan status alert.
- Pencatatan investigasi dan tindak lanjut.
- Search, filter severity/source, dan pagination event.
- Validasi JSON, field wajib, enum, foreign key, serta format error konsisten.
- Automated tests dengan pytest.
- Dokumentasi API menggunakan OpenAPI 3.0.3.

## 3. Struktur Folder

```text
CyberSOC_API/
|-- app/
|   |-- controllers/
|   |   `-- api.py
|   |-- models/
|   |-- services/
|   |   `-- common.py
|   `-- extensions.py
|-- docs/
|   |-- erd.md
|   |-- openapi.yaml
|   `-- requests.http
|-- scripts/
|   |-- init_db.py
|   `-- seed.py
|-- tests/
|   |-- conftest.py
|   `-- test_api.py
|-- config.py
|-- run.py
|-- requirements.txt
|-- README.md
`-- REPORT.md
```

## 4. Persyaratan Sistem

Sebelum menjalankan aplikasi, pastikan perangkat sudah memiliki:

- Python 3.x
- pip
- Git (opsional, jika melakukan clone repository)

## 5. Instalasi dan Menjalankan Aplikasi

Jalankan perintah berikut melalui Windows PowerShell:

```powershell
# Clone repository
git clone https://github.com/abiyyushafy/CyberSOC_API.git

# Masuk ke direktori proyek
cd CyberSOC_API

# Membuat virtual environment
py -m venv venv

# Mengaktifkan virtual environment
.\venv\Scripts\Activate.ps1

# Menginstal dependency
py -m pip install -r requirements.txt

# Inisialisasi database
py scripts/init_db.py

# Mengisi data demonstrasi
py scripts/seed.py

# Menjalankan aplikasi
py run.py
```

Base URL:

`http://127.0.0.1:5000/api/v1`

Health check:

`GET /health`

## 6. Endpoint API

| Method | Endpoint | Fungsi |
|---|---|---|
| GET, POST | `/log-sources` | Daftar/buat sumber log |
| GET, PATCH, DELETE | `/log-sources/{id}` | Detail/ubah/hapus sumber |
| GET, POST | `/security-events` | Cari/ingest event |
| GET | `/security-events/{id}` | Detail event |
| GET, POST | `/detection-rules` | Daftar/buat aturan |
| PATCH | `/detection-rules/{id}` | Ubah aturan |
| GET, POST | `/alerts` | Daftar/buat alert |
| GET, PATCH | `/alerts/{id}` | Detail/ubah status alert |
| GET, POST | `/investigations` | Daftar/buat investigasi |
| PATCH | `/investigations/{id}` | Perbarui investigasi |

Dokumentasi spesifikasi API tersedia di `docs/openapi.yaml`.

## 7. Contoh Pencarian Event

Endpoint:

```http
GET /security-events?search=failed&severity=high&source_id=1&page=1&per_page=10
```

Parameter yang digunakan:

- `search`: mencari event berdasarkan kata kunci.
- `severity`: memfilter berdasarkan tingkat severity.
- `source_id`: memfilter berdasarkan sumber log.
- `page`: menentukan halaman.
- `per_page`: menentukan jumlah data per halaman.

Nilai `per_page` dibatasi maksimum 100.

## 8. Format Response

**Response berhasil:**

```json
{
  "success": true,
  "message": "Security event ingested",
  "data": {
    "id": 1
  }
}
```

**Response gagal:**

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Required fields are missing",
    "details": {
      "fields": ["message"]
    }
  }
}
```

## 9. Status HTTP

| Kode | Keterangan |
|---|---|
| 200 | Berhasil membaca, memperbarui, atau menghapus data |
| 201 | Berhasil membuat resource |
| 404 | Resource tidak ditemukan |
| 409 | Konflik nama atau resource masih direferensikan |
| 415 | Content-Type bukan application/json |
| 422 | Validasi gagal |

## 10. Automated Testing

Pengujian otomatis menggunakan `pytest`.

Jalankan perintah berikut:

```powershell
py -m pytest -v
```

Pengujian meliputi:

1. Pembuatan log source berhasil.
2. Validasi input ketika data tidak memenuhi persyaratan.
3. Ingest security event dan pagination.
4. Validasi referensi detection rule ketika membuat alert.

**Hasil pengujian terakhir:**

| Keterangan | Hasil |
|---|---:|
| Total test | 4 |
| Passed | 4 |
| Failed | 0 |

Seluruh pengujian berhasil dijalankan dengan pytest.

## 11. Keamanan dan Batasan

API menggunakan ORM, validasi input, pemeriksaan foreign key, pembatasan pagination, dan error response yang tidak mengungkap traceback.

Data contoh menggunakan alamat dokumentasi `192.0.2.0/24`.

Sistem ini merupakan MVP edukasi dan belum memiliki:

- Autentikasi JWT.
- Role-Based Access Control (RBAC).
- Rate limiting.
- HTTPS deployment.
- Integrasi SIEM nyata.
- Log collector.

Jangan gunakan sistem ini untuk data produksi tanpa implementasi pengamanan tambahan.

Seluruh event dan aktivitas demonstrasi disimulasikan. Tidak ada scanning atau akses tanpa izin.

## 12. Rencana Pengembangan UAS

1. Implementasi JWT access/refresh token dan RBAC (SOC admin, analyst, viewer).
2. Rule engine otomatis yang mengevaluasi event terhadap detection rules.
3. Dashboard metrik event, alert, severity, dan tren.
4. Integrasi log collector pada host yang dimiliki atau diizinkan.
5. Notifikasi alert kritis.
6. Deployment HTTPS, secret management, rate limiting, dan backup.
7. Optimasi query, indeks, retensi, dan ekspor log.

## 13. Referensi dan Bantuan AI

- Flask: https://flask.palletsprojects.com/
- Flask-SQLAlchemy: https://flask-sqlalchemy.palletsprojects.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- OpenAPI: https://spec.openapis.org/oas/v3.0.3

ChatGPT (OpenAI) digunakan sebagai alat bantu dalam perancangan, pengembangan kode awal, dokumentasi, dan pengujian proyek.

## 14. GitHub Repository

Repository:

https://github.com/abiyyushafy/CyberSOC_API

**Clone repository:**

```bash
git clone https://github.com/abiyyushafy/CyberSOC_API.git
cd CyberSOC_API
```

**Mengirim perubahan terbaru ke GitHub:**

```bash
git add .
git commit -m "deskripsi perubahan"
git push origin main
```

**Versi proyek:** `v1.0.0`