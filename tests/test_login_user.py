import pytest
import allure
from api_client import ApiClient
from data import Message
from generators import generate_user_data

@allure.feature('Авторизация пользователя')
class TestLoginUser:
    
    @allure.title('Успешная авторизация существующего пользователя')
    def test_login_success(self):
        # Создаем пользователя
        user_data = generate_user_data()
        ApiClient.register_user(user_data)
        
        with allure.step("Выполняем авторизацию"):
            response = ApiClient.login_user(user_data["email"], user_data["password"])
            
        with allure.step("Проверяем успешный ответ"):
            assert response.status_code == 200
            assert response.json()["success"] == True
            assert response.json()["user"]["email"] == user_data["email"]
    
    @allure.title('Неудачная авторизация с неверным email')
    def test_login_invalid_email(self):
        user_data = generate_user_data()
        ApiClient.register_user(user_data)
        
        with allure.step("Пытаемся авторизоваться с неверным email"):
            response = ApiClient.login_user("invalid-email@example.com", user_data["password"])
            
        with allure.step("Проверяем ошибку авторизации"):
            assert response.status_code == 401
            assert response.json() == Message.LOGIN_FAILED
    
    @allure.title('Неудачная авторизация с неверным паролем')
    def test_login_invalid_password(self):
        user_data = generate_user_data()
        ApiClient.register_user(user_data)
        
        with allure.step("Пытаемся авторизоваться с неверным паролем"):
            response = ApiClient.login_user(user_data["email"], "wrong-password123")
            
        with allure.step("Проверяем ошибку авторизации"):
            assert response.status_code == 401
            assert response.json() == Message.LOGIN_FAILED