from flask import jsonify, request

def success(data=None, message="OK", status=200, meta=None):
    body = {"success": True, "message": message, "data": data}
    if meta is not None:
        body["meta"] = meta
    return jsonify(body), status

def failure(message, status=400, code="VALIDATION_ERROR", details=None):
    error = {"code": code, "message": message}
    if details is not None:
        error["details"] = details
    return jsonify({"success": False, "error": error}), status

def body_json():
    if not request.is_json:
        return None, failure("Content-Type must be application/json", 415, "UNSUPPORTED_MEDIA_TYPE")
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return None, failure("Request body must be a JSON object", 400, "INVALID_JSON")
    return payload, None

def missing_fields(payload, fields):
    return [field for field in fields if payload.get(field) in (None, "")]
