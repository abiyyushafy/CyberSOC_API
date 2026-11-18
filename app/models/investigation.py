from datetime import datetime, timezone
from app.extensions import db

class Investigation(db.Model):
    __tablename__ = "investigations"
    id = db.Column(db.Integer, primary_key=True)
    alert_id = db.Column(db.Integer, db.ForeignKey("alerts.id"), nullable=False, index=True)
    analyst_name = db.Column(db.String(100), nullable=False)
    findings = db.Column(db.Text, nullable=False)
    action_taken = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default="open")
    started_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    closed_at = db.Column(db.DateTime, nullable=True)

    alert = db.relationship("Alert", back_populates="investigations")

    def to_dict(self):
        return {"id": self.id, "alert_id": self.alert_id, "analyst_name": self.analyst_name,
                "findings": self.findings, "action_taken": self.action_taken,
                "status": self.status, "started_at": self.started_at.isoformat(),
                "closed_at": self.closed_at.isoformat() if self.closed_at else None}
