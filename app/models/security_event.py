from datetime import datetime, timezone
from app.extensions import db

class SecurityEvent(db.Model):
    __tablename__ = "security_events"
    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer, db.ForeignKey("log_sources.id"), nullable=False, index=True)
    event_type = db.Column(db.String(50), nullable=False, index=True)
    severity = db.Column(db.String(10), nullable=False, default="low", index=True)
    source_ip = db.Column(db.String(45), nullable=True)
    destination_ip = db.Column(db.String(45), nullable=True)
    username = db.Column(db.String(80), nullable=True)
    message = db.Column(db.Text, nullable=False)
    occurred_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    source = db.relationship("LogSource", back_populates="events")
    alerts = db.relationship("Alert", back_populates="event")

    def to_dict(self):
        return {"id": self.id, "source_id": self.source_id, "event_type": self.event_type,
                "severity": self.severity, "source_ip": self.source_ip,
                "destination_ip": self.destination_ip, "username": self.username,
                "message": self.message, "occurred_at": self.occurred_at.isoformat()}
