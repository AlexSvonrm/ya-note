from pytest_django.asserts import assertRedirects 



def test_with_client(client):
    response = client.get('/')
    assert response.status_code == 200



def test_closed_page(admin_client):
    response = admin_client.get('/only-for-users/')
    assert response.status_code == 200 