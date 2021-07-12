from django.test import TestCase

class TestSetup(TestCase):
    def setUp(self):
        print('Test started')
        self.user = {
            "username": "username",
            "email":"email@gmail.com",
            "password":"password",
            "password2":"password",
        }

    def tearDown(self):
        print('Test finish')
        return super().tearDown()