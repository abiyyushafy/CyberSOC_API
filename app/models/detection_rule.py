from datetime import datetime, timezone
from app.extensions import db

class DetectionRule(db.Model):
    __tablename__ = "detection_rules"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    event_type = db.Column(db.String(50), nullable=False, index=True)
    severity_threshold = db.Column(db.String(10), nullable=False, default="medium")
    is_enabled = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    alerts = db.relationship("Alert", back_populates="rule")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description,
                "event_type": self.event_type, "severity_threshold": self.severity_threshold,
                "is_enabled": self.is_enabled, "created_at": self.created_at.isoformat()}
