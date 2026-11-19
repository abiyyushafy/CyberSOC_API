## 1. Analisis Masalah

Organisasi menerima log dari berbagai sumber seperti server, firewall, dan endpoint. Tanpa pencatatan terpusat, analis kesulitan menelusuri event, menerapkan aturan deteksi, memprioritaskan alert, dan mendokumentasikan investigasi.

CyberSOC API dikembangkan sebagai REST API untuk mengelola alur tersebut menggunakan data simulasi.

Pengguna sistem meliputi administrator SOC, analis keamanan, dan operator pemantauan.

Fitur utama meliputi registrasi sumber log, pencatatan event keamanan, pengelolaan aturan deteksi, pembuatan alert, serta pencatatan investigasi.

Batasan sistem: MVP belum mengumpulkan log secara otomatis, belum menerapkan rule engine otomatis, autentikasi JWT/RBAC, notifikasi, maupun deployment produksi.

## 2. ERD dan Database

Sistem menggunakan lima tabel utama:

1. `log_sources`: menyimpan sumber log, tipe, host, environment, dan status.
2. `security_events`: menyimpan event keamanan, tingkat severity, IP sumber/tujuan, username, pesan, dan waktu.
3. `detection_rules`: menyimpan aturan deteksi, tipe event, ambang severity, dan status aktif.
4. `alerts`: menyimpan alert yang menghubungkan event dengan aturan deteksi.
5. `investigations`: menyimpan analisis dan tindak lanjut alert.

Relasi antar tabel:

- `log_sources` 1:N `security_events`.
- `security_events` 1:N `alerts`.
- `detection_rules` 1:N `alerts`.
- `alerts` 1:N `investigations`.

Setiap tabel memiliki primary key, sedangkan foreign key digunakan untuk menjaga hubungan antar data.

ERD lengkap tersedia pada `docs/erd.md`.

## 3. Implementasi Flask, ORM, dan MVC

Aplikasi dikembangkan menggunakan Python Flask dan Flask-SQLAlchemy sebagai ORM.

Struktur aplikasi menerapkan pemisahan tanggung jawab:

- **Models:** berada pada `app/models`, digunakan untuk mendefinisikan struktur dan relasi database.
- **Controllers:** berada pada `app/controllers`, digunakan untuk menangani endpoint dan request API.
- **Services:** berada pada `app/services`, digunakan untuk helper respons dan validasi.
- **Extensions:** berada pada `app/extensions.py`, digunakan untuk konfigurasi ekstensi aplikasi.

Database lokal menggunakan SQLite.

Endpoint API mencakup:

- `/log-sources`
- `/security-events`
- `/detection-rules`
- `/alerts`
- `/investigations`

HTTP method yang digunakan adalah GET, POST, PATCH, dan DELETE.

Status HTTP yang digunakan meliputi 200, 201, 404, 409, 415, dan 422.

## 4. Validasi, Keamanan, dan Testing

API menerapkan validasi Content-Type JSON, field wajib, severity, status, environment, dan keberadaan foreign key.

Format error response dibuat konsisten untuk mempermudah penanganan kesalahan oleh client.

SQLAlchemy ORM digunakan untuk mengakses database tanpa menyusun query SQL mentah berdasarkan input pengguna.

Pengujian otomatis menggunakan pytest dengan skenario:

1. Pengujian keberhasilan membuat sumber log.
2. Pengujian kegagalan validasi input.
3. Pengujian ingest event dan pagination.
4. Pengujian validasi referensi detection rule saat membuat alert.

**Hasil pengujian terakhir:**

| Keterangan | Hasil |
|---|---:|
| Total pengujian | 4 |
| Berhasil (Passed) | 4 |
| Gagal (Failed) | 0 |

Seluruh pengujian otomatis berhasil dijalankan.

## 5. Dokumentasi dan Publikasi

Dokumentasi proyek terdiri dari:

- `README.md`: berisi deskripsi proyek, instalasi, konfigurasi, cara menjalankan aplikasi, endpoint, contoh response, dan pengujian.
- `docs/erd.md`: dokumentasi Entity Relationship Diagram.
- `docs/openapi.yaml`: spesifikasi API menggunakan OpenAPI 3.0.3.
- `docs/requests.http`: contoh request untuk pengujian endpoint.
- `REPORT.md`: laporan implementasi proyek.

Repository GitHub:

https://github.com/abiyyushafy/CyberSOC_API

Kode sumber dan dokumentasi telah dipublikasikan melalui repository GitHub tersebut. Release versi v1.0.0 direncanakan setelah seluruh dokumentasi dan pemeriksaan akhir selesai.

Aplikasi saat ini berjalan pada lingkungan lokal dan belum di-deploy ke hosting publik.

## 6. Rencana Pengembangan UAS

Pengembangan lanjutan yang direncanakan meliputi:

1. Implementasi JWT access/refresh token dan Role-Based Access Control (RBAC).
2. Pengembangan rule engine otomatis untuk mengevaluasi event terhadap detection rules.
3. Dashboard SOC untuk menampilkan metrik event, alert, severity, dan tren.
4. Integrasi log collector pada sistem yang dimiliki atau telah mendapatkan izin.
5. Notifikasi untuk alert kritis.
6. Deployment HTTPS, secret management, rate limiting, dan backup.
7. Optimasi query, indeks database, retensi, dan ekspor log.

## 7. Kesimpulan

CyberSOC API merupakan MVP REST API untuk mendukung alur monitoring event keamanan hingga investigasi alert.

Sistem memiliki lima tabel database yang saling berelasi, implementasi Flask dan ORM dengan pemisahan MVC, endpoint API, validasi input, format error response yang konsisten, pencarian, filter, pagination, dokumentasi OpenAPI, serta automated testing.

Berdasarkan pengujian menggunakan pytest, seluruh empat skenario pengujian berhasil dijalankan.

Meskipun demikian, pengembangan fitur keamanan dan deployment lanjutan masih diperlukan sebelum sistem dapat digunakan pada lingkungan produksi.

## Referensi dan Bantuan AI

1. Flask Documentation: https://flask.palletsprojects.com/
2. Flask-SQLAlchemy: https://flask-sqlalchemy.palletsprojects.com/
3. SQLAlchemy: https://docs.sqlalchemy.org/
4. OpenAPI Specification 3.0.3: https://spec.openapis.org/oas/v3.0.3

ChatGPT (OpenAI) digunakan sebagai alat bantu dalam perancangan, pengembangan kode awal, dokumentasi, dan pengujian proyek.