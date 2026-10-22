import pytest
import requests
from generators import generate_user_data
from urls import URL

@pytest.fixture(scope="function")
def order_context():
    """
    Фикстура подготавливает всё необходимое для тестов создания заказа:
    1. Создает пользователя.
    2. Логинит его (получает токен).
    3. Получает актуальный список ингредиентов.
    4. Возвращает токен и ID валидного ингредиента.
    5. Удаляет пользователя после теста (очистка).
    """
    user_data = generate_user_data()
    
    # 1. Регистрация
    reg_resp = requests.post(URL.REGISTER_USER_URL, json=user_data)
    assert reg_resp.status_code == 200, f"Не удалось зарегистрировать пользователя: {reg_resp.text}"

    # 2. Авторизация (получение токена)
    login_resp = requests.post(URL.LOGIN_USER_URL, json={
        "email": user_data["email"],
        "password": user_data["password"]
    })
    assert login_resp.status_code == 200, f"Не удалось авторизоваться: {login_resp.text}"
    
    access_token = login_resp.json()["accessToken"]

    # 3. Получение ингредиентов
    ingredients_resp = requests.get(URL.INGREDIENTS_URL) # Проверь правильный URL в urls.py
    assert ingredients_resp.status_code == 200, f"Не удалось получить ингредиенты: {ingredients_resp.text}"
    
    ingredients_list = ingredients_resp.json().get('data', )
    if not ingredients_list:
        raise ValueError("Список ингредиентов пуст!")
    
    valid_ingredient_id = ingredients_list[0]["_id"]

    # Yield возвращает данные в тест
    yield {
        "token": access_token,
        "ingredient_id": valid_ingredient_id
    }

    # 4. Очистка (удаление пользователя)
    delete_resp = requests.delete(
        URL.REGISTER_USER_URL, 
        headers={"Authorization": f"Bearer {access_token}"}
    )