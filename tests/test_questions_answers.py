def test_question_create_and_list(client):
    r = client.post("/questions/", json={"text": "Q1"})
    assert r.status_code == 201
    q = r.json()
    assert q["id"] > 0
    assert q["text"] == "Q1"
    assert "created_at" in q

    r2 = client.get("/questions/")
    assert r2.status_code == 200
    data = r2.json()
    assert isinstance(data, list)
    assert len(data) == 1


def test_get_question_returns_answers(client):
    q = client.post("/questions/", json={"text": "Q1"}).json()

    a1 = client.post(f"/questions/{q['id']}/answers/", json={"user_id": "u1", "text": "A1"})
    assert a1.status_code == 201
    a2 = client.post(f"/questions/{q['id']}/answers/", json={"user_id": "u1", "text": "A2"})
    assert a2.status_code == 201

    r = client.get(f"/questions/{q['id']}")
    assert r.status_code == 200
    payload = r.json()
    assert payload["id"] == q["id"]
    assert payload["text"] == "Q1"
    assert "answers" in payload
    assert len(payload["answers"]) == 2


def test_cannot_create_answer_for_missing_question(client):
    r = client.post("/questions/9999/answers/", json={"user_id": "u1", "text": "A1"})
    assert r.status_code == 404


def test_delete_question_cascades_answers(client):
    q = client.post("/questions/", json={"text": "Q1"}).json()
    a = client.post(f"/questions/{q['id']}/answers/", json={"user_id": "u1", "text": "A1"}).json()

    d = client.delete(f"/questions/{q['id']}")
    assert d.status_code == 204

    # Answer should be gone after question deletion (cascade).
    r = client.get(f"/answers/{a['id']}")
    assert r.status_code == 404


def test_delete_answer(client):
    q = client.post("/questions/", json={"text": "Q1"}).json()
    a = client.post(f"/questions/{q['id']}/answers/", json={"user_id": "u1", "text": "A1"}).json()

    d = client.delete(f"/answers/{a['id']}")
    assert d.status_code == 204

    r = client.get(f"/answers/{a['id']}")
    assert r.status_code == 404


def test_validation_rejects_empty_text(client):
    r = client.post("/questions/", json={"text": ""})
    assert r.status_code == 422

    q = client.post("/questions/", json={"text": "Q1"}).json()
    r2 = client.post(f"/questions/{q['id']}/answers/", json={"user_id": "u1", "text": ""})
    assert r2.status_code == 422
