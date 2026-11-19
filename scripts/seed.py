import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from run import app
from app.extensions import db
from app.models import LogSource, SecurityEvent, DetectionRule, Alert, Investigation

with app.app_context():
    db.create_all()
    if LogSource.query.first():
        print("Seed skipped: log sources already exist.")
    else:
        source = LogSource(name="Demo Linux Server", source_type="linux_syslog",
                           host="demo-server.local", environment="staging", status="active")
        rule = DetectionRule(name="Repeated Failed Login",
            description="Detects simulated repeated authentication failures.",
            event_type="authentication_failure", severity_threshold="high", is_enabled=True)
        db.session.add_all([source, rule])
        db.session.flush()
        event = SecurityEvent(source_id=source.id, event_type="authentication_failure",
            severity="high", source_ip="192.0.2.55", destination_ip="192.0.2.10",
            username="demo-user", message="Synthetic event: repeated failed login attempts.")
        db.session.add(event)
        db.session.flush()
        alert = Alert(event_id=event.id, rule_id=rule.id,
            title="Possible brute-force activity (simulation)", severity="high", status="new")
        db.session.add(alert)
        db.session.flush()
        investigation = Investigation(alert_id=alert.id, analyst_name="SOC Analyst Demo",
            findings="Synthetic investigation record; no real host was accessed.",
            action_taken="Recorded for demonstration", status="open")
        db.session.add(investigation)
        db.session.commit()
        print("Synthetic seed data inserted.")
