import sys
import os
import unittest
from unittest.mock import patch, MagicMock
from app import create_app, db
from app.models.file import File, FileService

class TestFileManager(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.file_service = FileService()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @patch('file_manager.magic.Magic')
    def test_identify_file_type(self, mock_magic):
        mock_magic_instance = MagicMock()
        mock_magic.return_value = mock_magic_instance

        mock_magic_instance.from_file.return_value = 'audio/mpeg'
        self.assertEqual(File.identify_file_type('test.mp3'), 'audio')

        mock_magic_instance.from_file.return_value = 'video/mp4'
        self.assertEqual(File.identify_file_type('test.mp4'), 'video')

        mock_magic_instance.from_file.return_value = 'image/jpeg'
        self.assertEqual(File.identify_file_type('test.jpg'), 'imagen')

        mock_magic_instance.from_file.return_value = 'text/plain'
        self.assertEqual(File.identify_file_type('test.txt'), 'desconocido')

    @patch('file_manager.File.identify_file_type')
    @patch('file_manager.shutil.move')
    def test_move_file(self, mock_move, mock_identify):
        mock_identify.return_value = 'audio'
        base_dir = '/tmp/base'
        new_path = File.move_file('/tmp/test_audio.mp3', base_dir)
        self.assertEqual(new_path, os.path.join(base_dir, 'audio', 'test_audio.mp3'))
        mock_move.assert_called_once()

    def test_file_crud(self):
        file = File(id_name='test123', realname='test.txt', filetype='txt', user_id=1)
        
        # Create
        self.file_service.save(file)
        self.assertIsNotNone(file.id_name)

        # Read
        found_file = self.file_service.find(file.id_name)
        self.assertIsNotNone(found_file)
        self.assertEqual(found_file.realname, 'test.txt')

        # Update
        file.realname = 'updated.txt'
        self.file_service.update(file, file.id_name)
        updated_file = self.file_service.find(file.id_name)
        self.assertEqual(updated_file.realname, 'updated.txt')

        # Delete
        self.file_service.delete(file)
        self.assertIsNone(self.file_service.find(file.id_name))

    def test_sanitize_filename(self):
        with self.assertRaises(ValueError):
            self.file_service.sanitize_filename("Test File!@#.txt")

        self.assertEqual(self.file_service.sanitize_filename("valid_file_name"), "valid_file_name")
        self.assertEqual(self.file_service.sanitize_filename("UPPERCASE_FILE"), "uppercase_file")

    def test_validate_extension(self):
        self.assertEqual(self.file_service.validate_extension("pdf"), "pdf")
        with self.assertRaises(ValueError):
            self.file_service.validate_extension("exe")

    def test_generate_unique_filename(self):
        unique_name = self.file_service.generate_unique_filename("test", "txt")
        self.assertIn("test", unique_name)
        self.assertIn("txt", unique_name)
        self.assertGreater(len(unique_name), len("test") + len("txt") + 1)

if __name__ == '__main__':
    unittest.main()