def test_get_delivery_history_empty(client, auth_headers):
    response = client.get('/deliver/history', headers=auth_headers)
    assert response.status_code == 200
    assert response.json['history'] == []

def test_send_email_missing_fields(client, auth_headers):
    response = client.post('/deliver/email', 
                          headers=auth_headers,
                          json={})
    assert response.status_code == 400

def test_send_whatsapp_missing_fields(client, auth_headers):
    response = client.post('/deliver/whatsapp',
                          headers=auth_headers,
                          json={})
    assert response.status_code == 400
