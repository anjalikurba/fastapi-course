def test_create_user(client):
    data ={"email":"pingpong@gmail.com","password":"123456"}
    response = client.post("/user/",json=data)
    assert response.status_code == 201
    assert response.json()["email"]=="pingpong@gmail.com"
