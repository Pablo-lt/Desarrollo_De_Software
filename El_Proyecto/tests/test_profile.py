import os
import unittest
from app import create_app, db
from app.models import Profile
from app.services import ProfileService
from .utils import utils

profile_service = ProfileService()

class ProfileTestCase(unittest.TestCase):
    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.NAME = "Client"
        self.sample_user = utils.create_test_user()
        db.session.add(self.sample_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_profile_save(self):
        profile = Profile(name=self.NAME)
        saved_profile = profile_service.save(profile, self.sample_user)
        self.assertGreaterEqual(saved_profile.id, 1)
        self.assertEqual(saved_profile.name, self.NAME)
        self.assertEqual(saved_profile.created_by_id, self.sample_user.id)

    def test_profile_delete(self):
        profile = Profile(name=self.NAME)
        saved_profile = profile_service.save(profile, self.sample_user)
        profile_service.delete(saved_profile, self.sample_user)
        self.assertIsNone(profile_service.find(saved_profile.id))

    def test_profile_update(self):
        profile = Profile(name=self.NAME)
        saved_profile = profile_service.save(profile, self.sample_user)
    
        # Crear un nuevo objeto Profile con los datos actualizados
        updated_profile_data = Profile(name="Client Updated")
    
        # Llamar al método update con el nuevo objeto, el id del perfil guardado y el usuario
        updated_profile = profile_service.update(updated_profile_data, saved_profile.id, self.sample_user)
    
        # Verificar que la actualización fue exitosa
        self.assertEqual(updated_profile.name, "Client Updated")

    def test_profile_find(self):
        profile = Profile(name=self.NAME)
        saved_profile = profile_service.save(profile, self.sample_user)
        found_profile = profile_service.find(saved_profile.id)
        self.assertIsNotNone(found_profile)

    def test_all(self):
        profile = Profile(name=self.NAME)
        profile_service.save(profile, self.sample_user)
        profiles = profile_service.all()
        self.assertGreaterEqual(len(profiles), 1)

    def test_profile_save_sets_audit_fields(self):
        # Crea y guarda un nuevo perfil
        profile = Profile(name=self.NAME)
        saved_profile = profile_service.save(profile, self.sample_user)

        # Verifica que los campos de auditoría se hayan establecido correctamente
        self.assertIsNotNone(saved_profile.created_at)
        self.assertIsNotNone(saved_profile.updated_at)
        self.assertEqual(saved_profile.created_by_id, self.sample_user.id)
        self.assertEqual(saved_profile.updated_by_id, self.sample_user.id)
        # Verifica que created_at y updated_at sean iguales en la creación
        self.assertEqual(saved_profile.created_at, saved_profile.updated_at)

    def test_profile_update_modifies_audit_fields(self):
        # Crea y guarda un perfil inicial
        profile = Profile(name=self.NAME)
        saved_profile = profile_service.save(profile, self.sample_user)
        
        # Guarda los valores originales de auditoría
        original_updated_at = saved_profile.updated_at
        original_updated_by_id = saved_profile.updated_by_id

        # Actualiza el perfil
        updated_profile_data = Profile(name="Updated Name")
        updated_profile = profile_service.update(updated_profile_data, saved_profile.id, self.sample_user)

        # Verifica que los campos de auditoría se hayan actualizado correctamente
        self.assertNotEqual(updated_profile.updated_at, original_updated_at)
        self.assertEqual(updated_profile.updated_by_id, self.sample_user.id)
        # Verifica que los campos de creación no hayan cambiado
        self.assertEqual(updated_profile.created_at, saved_profile.created_at)
        self.assertEqual(updated_profile.created_by_id, saved_profile.created_by_id)

    def test_profile_delete_updates_audit_fields(self):
        # Crea y guarda un perfil inicial
        profile = Profile(name=self.NAME)
        saved_profile = profile_service.save(profile, self.sample_user)
        
        # Guarda el valor original de updated_at
        original_updated_at = saved_profile.updated_at
        
        # Elimina el perfil (soft delete)
        profile_service.delete(saved_profile, self.sample_user)
        
        # Intenta recuperar el perfil eliminado
        deleted_profile = profile_service.find(saved_profile.id)
        
        # Verifica que el perfil aún existe (soft delete) y que los campos de auditoría se actualizaron
        self.assertIsNotNone(deleted_profile)
        self.assertNotEqual(deleted_profile.updated_at, original_updated_at)
        self.assertEqual(deleted_profile.updated_by_id, self.sample_user.id)
        # Verifica que los campos de creación no hayan cambiado
        self.assertEqual(deleted_profile.created_at, saved_profile.created_at)
        self.assertEqual(deleted_profile.created_by_id, saved_profile.created_by_id)
        
if __name__ == '__main__':
    unittest.main()