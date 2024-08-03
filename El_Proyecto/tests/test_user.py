import os
import unittest
from flask import current_app
from app import create_app, db
from app.services import UserService
from .utils import utils 

user_service = UserService()

class UserTestCase(unittest.TestCase):
    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.sample_user = utils.create_test_user()  
        self.utils= utils

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app(self):
        self.assertIsNotNone(current_app)

    def test_user(self):  
        user = self.sample_user
        self.assertEqual(user.email, utils.EMAIL_PRUEBA)
        self.assertEqual(user.username, utils.USERNAME_PRUEBA)
        self.assertEqual(user.password, utils.PASSWORD_PRUEBA)
        self.assertIsNotNone(user.data)
        self.assertEqual(user.data.firstname, utils.FIRSTNAME_PRUEBA )
        self.assertEqual(user.data.lastname, utils.LASTNAME_PRUEBA)
        self.assertEqual(user.data.phone, utils.PHONE_PRUEBA)
        self.assertEqual(user.data.description, utils.DESCRIPTION)

    def test_user_save(self):
        user = self.sample_user
        user_service.save(user)
        self.assertGreaterEqual(user.id, 1)
        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(user.username, 'pabloprats')
        self.assertIsNotNone(user.password)
        self.assertTrue(user_service.check_auth(user.username, '123456'))

    def test_user_delete(self):
        user = self.sample_user
        user_service.save(user)
        user_service.delete(user)
        self.assertIsNone(user_service.find(user))

    def test_user_all(self):
        user_service.save(self.sample_user)
        users = user_service.all()
        self.assertGreaterEqual(len(users), 1)

    def test_user_find(self):
        user_service.save(self.sample_user)
        user_find = user_service.find(1)
        self.assertIsNotNone(user_find)
        self.assertEqual(user_find.id, self.sample_user.id)
        self.assertEqual(user_find.email, self.sample_user.email)

if __name__ == '__main__':
    unittest.main()