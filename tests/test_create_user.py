import pytest
import allure
from generators import generate_user_data
from api_client import ApiClient
from data import Message

class TestCreateUser:
    
    @allure.title("Успешная регистрация нового пользователя")
    def test_register_new_user(self):
        user_data = generate_user_data()
        
        response = ApiClient.register_user(user_data)
        assert response.status_code == 200
        assert response.json()["success"] == True
        assert response.json()["user"]["email"] == user_data["email"]
    
    @allure.title("Регистрация существующего пользователя")
    def test_register_existing_user(self):
        user_data = generate_user_data()
        ApiClient.register_user(user_data)
        
        response = ApiClient.register_user(user_data)
        assert response.status_code == 403
        assert response.json() == Message.USER_EXISTS
    
    @pytest.mark.parametrize('missing_field', ['email', 'password', 'name'])
    @allure.title("Регистрация без обязательного поля")
    def test_register_missing_field(self, missing_field):
        user_data = generate_user_data()
        del user_data[missing_field]
        
        response = ApiClient.register_user(user_data)
        assert response.status_code == 403
        assert response.json() == Message.MISSING_FIELDS