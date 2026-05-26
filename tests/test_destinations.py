URL = "/destinations"


def add(client, destination="Paris", country="France", rating=4.5):
    return client.post(URL, json={"destination": destination, "country": country, "rating": rating})


def test_get_all_empty(client):
    assert client.get(URL).status_code == 200
    assert client.get(URL).get_json() == []


def test_get_all_returns_list(client):
    add(client)
    add(client, destination="Tokyo", country="Japan", rating=5.0)
    assert len(client.get(URL).get_json()) == 2


def test_get_one(client):
    id_ = add(client).get_json()["id"]
    r = client.get(f"{URL}/{id_}")
    assert r.status_code == 200
    assert r.get_json()["destination"] == "Paris"


def test_get_one_not_found(client):
    assert client.get(f"{URL}/9999").status_code == 404


def test_create_success(client):
    r = add(client)
    assert r.status_code == 201
    body = r.get_json()
    assert body["destination"] == "Paris"
    assert body["country"] == "France"
    assert body["rating"] == 4.5
    assert "id" in body


def test_create_missing_fields(client):
    r = client.post(URL, json={"destination": "Paris"})
    assert r.status_code == 422
    assert "details" in r.get_json()


def test_create_rating_out_of_range(client):
    assert add(client, rating=6.0).status_code == 422


def test_create_rating_negative(client):
    assert add(client, rating=-1.0).status_code == 422


def test_create_non_json_body(client):
    r = client.post(URL, data="not json", content_type="text/plain")
    assert r.status_code == 400


def test_create_empty_destination_name(client):
    r = client.post(URL, json={"destination": "  ", "country": "France", "rating": 4.0})
    assert r.status_code == 422


def test_update_rating(client):
    id_ = add(client).get_json()["id"]
    r = client.put(f"{URL}/{id_}", json={"rating": 4.9})
    assert r.status_code == 200
    assert r.get_json()["rating"] == 4.9


def test_update_multiple_fields(client):
    id_ = add(client).get_json()["id"]
    r = client.put(f"{URL}/{id_}", json={"destination": "Lyon", "rating": 3.8})
    assert r.status_code == 200
    body = r.get_json()
    assert body["destination"] == "Lyon"
    assert body["rating"] == 3.8


def test_update_not_found(client):
    assert client.put(f"{URL}/9999", json={"rating": 4.0}).status_code == 404


def test_update_invalid_rating(client):
    id_ = add(client).get_json()["id"]
    assert client.put(f"{URL}/{id_}", json={"rating": 99}).status_code == 422


def test_delete_success(client):
    id_ = add(client).get_json()["id"]
    assert client.delete(f"{URL}/{id_}").status_code == 204


def test_delete_removes_resource(client):
    id_ = add(client).get_json()["id"]
    client.delete(f"{URL}/{id_}")
    assert client.get(f"{URL}/{id_}").status_code == 404


def test_delete_not_found(client):
    assert client.delete(f"{URL}/9999").status_code == 404
