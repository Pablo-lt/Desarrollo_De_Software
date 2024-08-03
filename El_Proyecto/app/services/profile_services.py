from typing import List
from app.models import Profile, User
from app.repository import ProfileRepository
from datetime import datetime, timezone

repository = ProfileRepository()

class ProfileService:
    def save(self, profile: Profile, user: User) -> Profile:
        profile.created_by_id = user.id
        profile.updated_by_id = user.id
        profile.created_at = datetime.now(timezone.utc)
        profile.updated_at = datetime.now(timezone.utc)
        
        return repository.save(profile)

    def update(self, profile: Profile, id: int, user: User) -> Profile:
        existing_profile = repository.find(id)
        if existing_profile:
            existing_profile.updated_by_id = user.id
            existing_profile.updated_at = datetime.now(timezone.utc)
            existing_profile.name = profile.name 
            return repository.update(existing_profile, id)
        return None

    def delete(self, profile: Profile, user: User) -> None:
        profile.updated_by_id = user.id
        profile.updated_at = datetime.now(timezone.utc)
        
        repository.delete(profile)

    def all(self) -> List[Profile]:
        return repository.all()

    def find(self, id: int) -> Profile:
        return repository.find(id)