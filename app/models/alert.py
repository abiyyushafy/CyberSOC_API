from datetime import datetime, timezone
from app.extensions import db

class Alert(db.Model):
    __tablename__ = "alerts"
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("security_events.id"), nullable=False, index=True)
    rule_id = db.Column(db.Integer, db.ForeignKey("detection_rules.id"), nullable=False, index=True)
    title = db.Column(db.String(160), nullable=False)
    severity = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="new", index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    event = db.relationship("SecurityEvent", back_populates="alerts")
    rule = db.relationship("DetectionRule", back_populates="alerts")
    investigations = db.relationship("Investigation", back_populates="alert")

    def to_dict(self):
        return {"id": self.id, "event_id": self.event_id, "rule_id": self.rule_id,
                "title": self.title, "severity": self.severity, "status": self.status,
                "created_at": self.created_at.isoformat()}
