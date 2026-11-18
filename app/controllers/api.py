from datetime import datetime, timezone
from flask import Blueprint, request
from sqlalchemy import or_
from app.extensions import db
from app.models import LogSource, SecurityEvent, DetectionRule, Alert, Investigation
from app.services.common import success, failure, body_json, missing_fields

api_bp = Blueprint("api", __name__)
SEVERITIES = {"low", "medium", "high", "critical"}

@api_bp.get("/health")
def health():
    return success({"status": "healthy"}, "CyberSOC API is running")

def get_item(model, item_id):
    return db.session.get(model, item_id)

# Log sources
@api_bp.get("/log-sources")
def list_sources():
    return success([x.to_dict() for x in LogSource.query.order_by(LogSource.id).all()])

@api_bp.post("/log-sources")
def create_source():
    p, err = body_json()
    if err: return err
    missing = missing_fields(p, ["name", "source_type", "host"])
    if missing: return failure("Required fields are missing", 422, details={"fields": missing})
    if LogSource.query.filter_by(name=p["name"].strip()).first():
        return failure("Log source name already exists", 409, "DUPLICATE_RESOURCE")
    env = p.get("environment", "staging")
    if env not in {"development", "staging", "production"}: return failure("Invalid environment", 422)
    x = LogSource(name=p["name"].strip(), source_type=p["source_type"], host=p["host"],
                  environment=env, status=p.get("status", "active"))
    db.session.add(x); db.session.commit()
    return success(x.to_dict(), "Log source created", 201)

@api_bp.get("/log-sources/<int:item_id>")
def get_source(item_id):
    x = get_item(LogSource, item_id)
    return success(x.to_dict()) if x else failure("Log source not found", 404, "NOT_FOUND")

@api_bp.patch("/log-sources/<int:item_id>")
def update_source(item_id):
    x = get_item(LogSource, item_id)
    if not x: return failure("Log source not found", 404, "NOT_FOUND")
    p, err = body_json()
    if err: return err
    for key in ("name", "source_type", "host", "environment", "status"):
        if key in p: setattr(x, key, p[key])
    if x.environment not in {"development", "staging", "production"} or x.status not in {"active", "inactive"}:
        return failure("Invalid environment or status", 422)
    db.session.commit()
    return success(x.to_dict(), "Log source updated")

@api_bp.delete("/log-sources/<int:item_id>")
def delete_source(item_id):
    x = get_item(LogSource, item_id)
    if not x: return failure("Log source not found", 404, "NOT_FOUND")
    if x.events: return failure("Log source has events and cannot be deleted", 409, "RESOURCE_IN_USE")
    db.session.delete(x); db.session.commit()
    return success({"id": item_id}, "Log source deleted")

# Security events
@api_bp.get("/security-events")
def list_events():
    q = SecurityEvent.query
    term = request.args.get("search", "").strip()
    if term:
        like = f"%{term}%"
        q = q.filter(or_(SecurityEvent.event_type.ilike(like),
                         SecurityEvent.username.ilike(like), SecurityEvent.message.ilike(like)))
    severity = request.args.get("severity")
    if severity:
        if severity not in SEVERITIES: return failure("Invalid severity filter", 422)
        q = q.filter_by(severity=severity)
    source_id = request.args.get("source_id", type=int)
    if source_id: q = q.filter_by(source_id=source_id)
    page = max(request.args.get("page", 1, type=int), 1)
    per_page = min(max(request.args.get("per_page", 10, type=int), 1), 100)
    result = q.order_by(SecurityEvent.occurred_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return success([x.to_dict() for x in result.items], meta={
        "page": page, "per_page": per_page, "total": result.total, "pages": result.pages})

@api_bp.post("/security-events")
def create_event():
    p, err = body_json()
    if err: return err
    missing = missing_fields(p, ["source_id", "event_type", "message"])
    if missing: return failure("Required fields are missing", 422, details={"fields": missing})
    if not get_item(LogSource, p["source_id"]): return failure("source_id does not exist", 422)
    severity = p.get("severity", "low")
    if severity not in SEVERITIES: return failure("Invalid severity", 422)
    x = SecurityEvent(source_id=p["source_id"], event_type=p["event_type"],
        severity=severity, source_ip=p.get("source_ip"), destination_ip=p.get("destination_ip"),
        username=p.get("username"), message=p["message"])
    db.session.add(x); db.session.commit()
    return success(x.to_dict(), "Security event ingested", 201)

@api_bp.get("/security-events/<int:item_id>")
def get_event(item_id):
    x = get_item(SecurityEvent, item_id)
    return success(x.to_dict()) if x else failure("Security event not found", 404, "NOT_FOUND")

# Detection rules
@api_bp.get("/detection-rules")
def list_rules():
    return success([x.to_dict() for x in DetectionRule.query.order_by(DetectionRule.id).all()])

@api_bp.post("/detection-rules")
def create_rule():
    p, err = body_json()
    if err: return err
    missing = missing_fields(p, ["name", "description", "event_type", "severity_threshold"])
    if missing: return failure("Required fields are missing", 422, details={"fields": missing})
    if p["severity_threshold"] not in SEVERITIES: return failure("Invalid severity_threshold", 422)
    if DetectionRule.query.filter_by(name=p["name"].strip()).first():
        return failure("Rule name already exists", 409, "DUPLICATE_RESOURCE")
    x = DetectionRule(name=p["name"].strip(), description=p["description"],
        event_type=p["event_type"], severity_threshold=p["severity_threshold"],
        is_enabled=p.get("is_enabled", True))
    db.session.add(x); db.session.commit()
    return success(x.to_dict(), "Detection rule created", 201)

@api_bp.patch("/detection-rules/<int:item_id>")
def update_rule(item_id):
    x = get_item(DetectionRule, item_id)
    if not x: return failure("Detection rule not found", 404, "NOT_FOUND")
    p, err = body_json()
    if err: return err
    for key in ("name", "description", "event_type", "is_enabled"):
        if key in p: setattr(x, key, p[key])
    if "severity_threshold" in p:
        if p["severity_threshold"] not in SEVERITIES: return failure("Invalid severity_threshold", 422)
        x.severity_threshold = p["severity_threshold"]
    db.session.commit()
    return success(x.to_dict(), "Detection rule updated")

# Alerts (created from an event and a matching rule)
@api_bp.get("/alerts")
def list_alerts():
    q = Alert.query
    if request.args.get("status"): q = q.filter_by(status=request.args["status"])
    if request.args.get("severity"):
        if request.args["severity"] not in SEVERITIES: return failure("Invalid severity", 422)
        q = q.filter_by(severity=request.args["severity"])
    return success([x.to_dict() for x in q.order_by(Alert.created_at.desc()).all()])

@api_bp.post("/alerts")
def create_alert():
    p, err = body_json()
    if err: return err
    missing = missing_fields(p, ["event_id", "rule_id", "title", "severity"])
    if missing: return failure("Required fields are missing", 422, details={"fields": missing})
    event = get_item(SecurityEvent, p["event_id"])
    rule = get_item(DetectionRule, p["rule_id"])
    if not event or not rule: return failure("event_id or rule_id does not exist", 422)
    if not rule.is_enabled: return failure("Detection rule is disabled", 422)
    if p["severity"] not in SEVERITIES: return failure("Invalid severity", 422)
    x = Alert(event_id=event.id, rule_id=rule.id, title=p["title"],
              severity=p["severity"], status=p.get("status", "new"))
    db.session.add(x); db.session.commit()
    return success(x.to_dict(), "Alert created", 201)

@api_bp.get("/alerts/<int:item_id>")
def get_alert(item_id):
    x = get_item(Alert, item_id)
    return success(x.to_dict()) if x else failure("Alert not found", 404, "NOT_FOUND")

@api_bp.patch("/alerts/<int:item_id>")
def update_alert(item_id):
    x = get_item(Alert, item_id)
    if not x: return failure("Alert not found", 404, "NOT_FOUND")
    p, err = body_json()
    if err: return err
    if "status" in p:
        if p["status"] not in {"new", "acknowledged", "investigating", "closed"}:
            return failure("Invalid alert status", 422)
        x.status = p["status"]
    db.session.commit()
    return success(x.to_dict(), "Alert updated")

# Investigations
@api_bp.get("/investigations")
def list_investigations():
    q = Investigation.query
    if request.args.get("status"): q = q.filter_by(status=request.args["status"])
    return success([x.to_dict() for x in q.order_by(Investigation.started_at.desc()).all()])

@api_bp.post("/investigations")
def create_investigation():
    p, err = body_json()
    if err: return err
    missing = missing_fields(p, ["alert_id", "analyst_name", "findings"])
    if missing: return failure("Required fields are missing", 422, details={"fields": missing})
    if not get_item(Alert, p["alert_id"]): return failure("alert_id does not exist", 422)
    x = Investigation(alert_id=p["alert_id"], analyst_name=p["analyst_name"],
                      findings=p["findings"], action_taken=p.get("action_taken"),
                      status=p.get("status", "open"))
    db.session.add(x); db.session.commit()
    return success(x.to_dict(), "Investigation created", 201)

@api_bp.patch("/investigations/<int:item_id>")
def update_investigation(item_id):
    x = get_item(Investigation, item_id)
    if not x: return failure("Investigation not found", 404, "NOT_FOUND")
    p, err = body_json()
    if err: return err
    if "findings" in p: x.findings = p["findings"]
    if "action_taken" in p: x.action_taken = p["action_taken"]
    if "status" in p:
        if p["status"] not in {"open", "in_progress", "resolved"}:
            return failure("Invalid investigation status", 422)
        x.status = p["status"]
        if x.status == "resolved": x.closed_at = datetime.now(timezone.utc)
    db.session.commit()
    return success(x.to_dict(), "Investigation updated")
