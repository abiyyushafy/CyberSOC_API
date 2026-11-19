def setup_source(client):
    return client.post("/api/v1/log-sources", json={
        "name": "Test Syslog", "source_type": "linux_syslog", "host": "test.local"
    })

def test_create_log_source_success(client):
    response = setup_source(client)
    assert response.status_code == 201
    assert response.get_json()["data"]["name"] == "Test Syslog"

def test_create_log_source_validation_error(client):
    response = client.post("/api/v1/log-sources", json={"name": "Incomplete"})
    assert response.status_code == 422
    assert response.get_json()["success"] is False

def test_ingest_event_and_pagination(client):
    setup_source(client)
    response = client.post("/api/v1/security-events", json={
        "source_id": 1, "event_type": "authentication_failure",
        "severity": "high", "message": "Synthetic failed login"
    })
    assert response.status_code == 201
    listing = client.get("/api/v1/security-events?page=1&per_page=5")
    assert listing.status_code == 200
    assert listing.get_json()["meta"]["total"] == 1

def test_create_alert_requires_existing_rule(client):
    setup_source(client)
    client.post("/api/v1/security-events", json={
        "source_id": 1, "event_type": "authentication_failure", "message": "Test event"
    })
    response = client.post("/api/v1/alerts", json={
        "event_id": 1, "rule_id": 999, "title": "Test alert", "severity": "high"
    })
    assert response.status_code == 422
