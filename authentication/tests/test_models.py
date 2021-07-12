from django.test import TestCase

from authentication.models import User

class TestModel(TestCase):
    def test_should_create_user(self):
        user = User.objects.create_user(
            username='username',
            email='email@app.com'
        )
        user.set_password('password12!')
        user.save()
        self.assertEqual(str(user),'email@app.com')