import unittest
import json
from ex1 import app 

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        # Створюємо тестовий клієнт з об'єкта app
        self.client = app.test_client()
        self.client.testing = True

    def test_login_success(self):
        """Завдання 3: Успішний вхід (200 OK)"""
        response = self.client.post('/login', 
                                    data=json.dumps({"username": "admin", "password": "secret"}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], "Login successful")

    def test_login_failure(self):
        """Завдання 4: Невірні дані (401 Unauthorized)"""
        response = self.client.post('/login', 
                                    data=json.dumps({"username": "wrong", "password": "wrong"}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()['message'], "Invalid credentials")

if __name__ == '__main__':
    unittest.main()