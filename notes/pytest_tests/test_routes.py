from pytest_lazy_fixtures import lf
from http import HTTPStatus
from pytest_django.asserts import assertRedirects
from django.test import TestCase
# import pytest_lazyfixture
#from pytest_lazyfixture import lazy_fixture
from django.urls import reverse
import pytest


@pytest.mark.parametrize(
    'name',  # Имя параметра функции.
    # Значения, которые будут передаваться в name.'users:logout',
    ('notes:home', 'users:login', 'users:signup')
)
# Указываем имя изменяемого параметра в сигнатуре теста.
def test_pages_availability_for_anonymous_user(client, name):
    url = reverse(name)  # Получаем ссылку на нужный адрес.
    response = client.get(url)  # Выполняем запрос.
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    ('notes:list', 'notes:add', 'notes:success')
)
def test_pages_availability_for_auth_user(not_author_client, name):
    url = reverse(name)
    response = not_author_client.get(url)
    assert response.status_code == HTTPStatus.OK


# # Параметризуем тестирующую функцию:
# @pytest.mark.parametrize(
#     'name',
#     ('notes:detail', 'notes:edit', 'notes:delete'),
# )
# def test_pages_availability_for_author(author_client, name, note):
#     url = reverse(name, args=(note.slug,))
#     response = author_client.get(url)
#     assert response.status_code == HTTPStatus.OK


# Добавляем к тесту ещё один декоратор parametrize; в его параметры
# нужно передать фикстуры-клиенты и ожидаемый код ответа для каждого клиента.
@pytest.mark.parametrize(
    # parametrized_client - название параметра, 
    # в который будут передаваться фикстуры;
    # Параметр expected_status - ожидаемый статус ответа.
    'parametrized_client, expected_status',
    # В кортеже с кортежами передаём значения для параметров:
    [
        (lf('not_author_client'), HTTPStatus.NOT_FOUND),
        (lf('author_client'), HTTPStatus.OK)
    ],
)
# Этот декоратор оставляем таким же, как в предыдущем тесте.
@pytest.mark.parametrize(
    'name',
    ('notes:detail', 'notes:edit', 'notes:delete'),
)
# В параметры теста добавляем имена parametrized_client и expected_status.
def test_pages_availability_for_different_users(
        parametrized_client, name, note, expected_status
):
    url = reverse(name, args=(note.slug,))
    # Делаем запрос от имени клиента parametrized_client:
    response = parametrized_client.get(url)
    # Ожидаем ответ страницы, указанный в expected_status:
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name, args',
    (
        ('notes:detail', lf('slug_for_args')),
        ('notes:edit', lf('slug_for_args')),
        ('notes:delete', lf('slug_for_args')),
        # ('notes:detail', pytest.lazy_fixture('slug_for_args')),
        # ('notes:edit', pytest.lazy_fixture('slug_for_args')),
        # ('notes:delete', pytest.lazy_fixture('slug_for_args')),
        ('notes:add', None),
        ('notes:success', None),
        ('notes:list', None),
    ),
)
# Передаём в тест анонимный клиент, name проверяемых страниц и args:
def test_redirects(client, name, args):
    login_url = reverse('users:login')
    # Теперь не надо писать никаких if и можно обойтись одним выражением.
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url) 
    