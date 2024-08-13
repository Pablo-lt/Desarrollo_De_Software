import os
import unittest
from app import create_app, db
from app.models import File
from app.services import FileService

file_service = FileService()

class FileTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.REALNAME = "test_file"
        self.FILETYPE = "txt"
        self.USER_ID = 1

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_file_save(self):
        file = self.__get_file()
        file_service.save(file)
        self.assertIsNotNone(file.id_name)
        self.assertEqual(file.realname, self.REALNAME)
        self.assertEqual(file.filetype, self.FILETYPE)

    def test_file_delete(self):
        file = self.__get_file()
        file_service.save(file)
        file_service.delete(file)
        self.assertIsNone(file_service.find(file.id_name))

    def test_file_update(self):
        file = self.__get_file()
        file_service.save(file)
        new_realname = "updated_file"
        file.realname = new_realname
        file_service.update(file, file.id_name)
        updated_file = file_service.find(file.id_name)
        self.assertEqual(updated_file.realname, new_realname)

    def test_file_find(self):
        file = self.__get_file()
        file_service.save(file)
        found_file = file_service.find(file.id_name)
        self.assertIsNotNone(found_file)
        self.assertEqual(found_file.realname, self.REALNAME)

    def test_all(self):
        file = self.__get_file()
        file_service.save(file)
        files = file_service.all()
        self.assertGreaterEqual(len(files), 1)

    def test_sanitize_filename(self):
        # Caso 1: Nombre de archivo con caracteres no permitidos
        dirty_name = "Test File!@#.txt"
        with self.assertRaises(ValueError):
            file_service.sanitize_filename(dirty_name)

        # Caso 2: Nombre de archivo válido
        valid_name = "valid_file_name"
        try:
            sanitized = file_service.sanitize_filename(valid_name)
            self.assertEqual(sanitized, valid_name.lower())
        except ValueError:
            self.fail("sanitize_filename raised ValueError unexpectedly!")

        # Caso 3: Nombre de archivo con mayúsculas (debería convertirse a minúsculas)
        upper_name = "UPPERCASE_FILE"
        try:
            sanitized = file_service.sanitize_filename(upper_name)
            self.assertEqual(sanitized, upper_name.lower())
        except ValueError:
            self.fail("sanitize_filename raised ValueError unexpectedly!")

    def test_validate_extension(self):
        valid_type = "pdf"
        invalid_type = "exe"
        self.assertEqual(file_service.validate_extension(valid_type), valid_type)
        with self.assertRaises(ValueError):
            file_service.validate_extension(invalid_type)

    def test_generate_unique_filename(self):
        unique_name = file_service.generate_unique_filename(self.REALNAME, self.FILETYPE)
        self.assertIn(self.REALNAME, unique_name)
        self.assertIn(self.FILETYPE, unique_name)
        self.assertGreater(len(unique_name), len(self.REALNAME) + len(self.FILETYPE) + 1)

    def __get_file(self) -> File:
        file = File()
        file.realname = self.REALNAME
        file.filetype = self.FILETYPE
        file.user_id = self.USER_ID
        return file

if __name__ == '__main__':
    unittest.main()