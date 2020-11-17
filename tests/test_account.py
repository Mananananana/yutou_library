import unittest

from flask import url_for

from .base import BaseTestCase
from yutou_library.models import User


class AccountTestCase(BaseTestCase):
    def test_register_validator(self):
        response = self.client.post(url_for('api_v1.register'))
        self.assertEqual(response.status_code, 400)

        response = self.client.post(url_for("api_v1.register"), json={"email": "121234hufwej",
                                                                      "phone": "13912345678",
                                                                      "password": "123456"})
        self.assertEqual(response.status_code, 400)

        response = self.client.post(url_for("api_v1.register"), json={"email": "123456@qq.com",
                                                                      "phone": "1391234678",
                                                                      "password": "123456"})
        self.assertEqual(response.status_code, 400)

        response = self.client.post(url_for("api_v1.register"), json={"email": "123456@qq.com",
                                                                      "phone": "13912345678",
                                                                      "password": "12345"})
        self.assertEqual(response.status_code, 400)

        response = self.client.post(url_for("api_v1.register"), json={"email": "123456@qq.com",
                                                                      "phone": "1f49h3qfhjs",
                                                                      "password": "123456"})
        self.assertEqual(response.status_code, 400)

        response = self.client.post(url_for("api_v1.register"), json={"email": "123456@qq.com",
                                                                      "phone": "13912345679",
                                                                      "password": "123456"})
        self.assertEqual(response.status_code, 400)

        response = self.client.post(url_for("api_v1.register"), json={"email": "1234567@qq.com",
                                                                      "phone": "13912345678",
                                                                      "password": "123456"})
        self.assertEqual(response.status_code, 400)

        response = self.client.post(url_for("api_v1.register"), json={"email": "1234567@qq.com",
                                                                      "phone": "13912345679",
                                                                      "password": "123456"})
        self.assertEqual(response.status_code, 201)

    def test_register(self):
        email = "1234567@qq.com"
        phone = "13912345679"
        password = "123456"
        response = self.client.post(url_for("api_v1.register"),
                                    json=dict(email=email, phone=phone, password=password))
        self.assertEqual(response.status_code, 201)
        user = User.query.filter_by(email=email, phone=phone).first()
        self.assertIsNotNone(user)
        self.assertTrue(user.validate_password(password))

    def test_login_method(self):
        response = self.client.post(url_for("api_v1.login"))
        self.assertEqual(response.status_code, 400)

        response = self.client.post(url_for("api_v1.login"), json={"method": "nothing"})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertTrue("method" in data["msg"])

        for method in ["email", "phone"]:
            response = self.client.post(url_for("api_v1.login"), json={"method": method})
            self.assertEqual(response.status_code, 401)

    def test_email_login(self):
        response = self.client.post(url_for("api_v1.login"), json={"method": "email",
                                                                   "email": "12341234123",
                                                                   "password": "123456"})
        self.assertEqual(response.status_code, 401)

        response = self.client.post(url_for("api_v1.login"), json={"method": "email",
                                                                   "email": "123456@qq.com",
                                                                   "password": "123456789"})
        self.assertEqual(response.status_code, 401)

        response = self.client.post(url_for("api_v1.login"), json={"method": "email",
                                                                   "email": "123456@qq.com",
                                                                   "password": "123456"})
        self.assertEqual(response.status_code, 201)

    def test_phone_login(self):
        response = self.client.post(url_for("api_v1.login"), json={"method": "phone",
                                                                   "phone": "1391234578",
                                                                   "password": "123456"})
        self.assertEqual(response.status_code, 401)

        response = self.client.post(url_for("api_v1.login"), json={"method": "phone",
                                                                   "phone": "13912345678",
                                                                   "password": "123456789"})
        self.assertEqual(response.status_code, 401)

        response = self.client.post(url_for("api_v1.login"), json={"method": "phone",
                                                                   "phone": "13912345678",
                                                                   "password": "123456"})
        self.assertEqual(response.status_code, 201)

    def test_get_info(self):
        token = self.get_token()
        response = self.client.get(url_for("api_v1.get_info"), headers=[("Authorization", "Bearer " + token)])
        data = response.get_json()
        self.assertEqual(data["name"], "laichaoqun")
        self.assertEqual(data["gender"], "male")
        self.assertEqual(data["phone"], "13912345678")
        self.assertEqual(data["email"], "123456@qq.com")
        self.assertTrue(isinstance(data["register_date"], int))
        self.assertFalse("password" in data or "_password" in data)

    def test_modify_info(self):
        token = self.get_token()
        response = self.client.patch(url_for("api_v1.modify_info"),
                                     json={"gender": "female", "name": "xiaohong"},
                                     headers=[('Authorization', "Bearer " + token)])
        self.assertEqual(response.status_code, 201)
        user = User.query.filter_by(phone="13912345678").first()
        self.assertIsNotNone(user)

        self.assertIsNotNone(user.gender)
        self.assertEqual(user.gender.value, "female")

        self.assertIsNotNone(user.name)
        self.assertEqual(user.name, "xiaohong")


if __name__ == "__main__":
    unittest.main()
