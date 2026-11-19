# ERD CyberSOC API

```mermaid
erDiagram
    LOG_SOURCES ||--o{ SECURITY_EVENTS : emits
    SECURITY_EVENTS ||--o{ ALERTS : triggers
    DETECTION_RULES ||--o{ ALERTS : matches
    ALERTS ||--o{ INVESTIGATIONS : examined_in

    LOG_SOURCES {
        int id PK
        string name UK
        string source_type
        string host
        string environment
        string status
        datetime created_at
    }
    SECURITY_EVENTS {
        int id PK
        int source_id FK
        string event_type
        string severity
        string source_ip
        string destination_ip
        string username
        text message
        datetime occurred_at
    }
    DETECTION_RULES {
        int id PK
        string name UK
        text description
        string event_type
        string severity_threshold
        boolean is_enabled
        datetime created_at
    }
    ALERTS {
        int id PK
        int event_id FK
        int rule_id FK
        string title
        string severity
        string status
        datetime created_at
    }
    INVESTIGATIONS {
        int id PK
        int alert_id FK
        string analyst_name
        text findings
        text action_taken
        string status
        datetime started_at
        datetime closed_at
    }
```

## Penjelasan relasi
- `log_sources.id` adalah PK; `name` unik. Satu sumber log menghasilkan banyak security event.
- `security_events.source_id` adalah FK ke `log_sources.id`.
- `detection_rules.id` adalah PK; `name` unik. Satu aturan deteksi dapat menghasilkan banyak alert.
- `alerts.event_id` dan `alerts.rule_id` adalah FK ke `security_events.id` dan `detection_rules.id`.
- `investigations.alert_id` adalah FK ke `alerts.id`. Satu alert dapat memiliki beberapa catatan investigasi.
- Penghapusan sumber log/event/aturan/alert yang masih direferensikan dicegah oleh integritas FK dan relasi.
