from datetime import datetime, timezone
from app.extensions import db

class LogSource(db.Model):
    __tablename__ = "log_sources"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    source_type = db.Column(db.String(40), nullable=False)
    host = db.Column(db.String(120), nullable=False)
    environment = db.Column(db.String(20), nullable=False, default="staging")
    status = db.Column(db.String(20), nullable=False, default="active")
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    events = db.relationship("SecurityEvent", back_populates="source")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "source_type": self.source_type,
                "host": self.host, "environment": self.environment, "status": self.status,
                "created_at": self.created_at.isoformat()}
