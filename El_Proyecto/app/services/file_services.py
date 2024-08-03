import uuid
from typing import List
from app.models import File
from app.repository import FileRepository

repository = FileRepository()

class FileService:
    """
    FileService class
    """
    def __init__(self):
        pass

    def sanitize_filename(self, filename: str) -> str:
        """
        Sanitize a filename and validate it only contains allowed characters
        :param filename: str
        :return: str
        :raises ValueError: If filename contains disallowed characters
        """
        sanitized = ''.join(c for c in filename if c.isalnum() or c in ('-', '_')).lower()
        if sanitized != filename.lower():
            raise ValueError("El nombre del archivo solo puede contener caracteres alfanuméricos, guiones y guiones bajos.")
        return sanitized

    def validate_extension(self, filetype: str) -> str:
        """
        Validate file extension
        :param filetype: str
        :return: str
        :raises ValueError: If file extension is not allowed
        """
        allowed_extensions = ['pdf', 'jpg', 'png', 'txt']
        if filetype.lower() not in allowed_extensions:
            raise ValueError(f"Extensión de archivo no permitida. Las extensiones permitidas son: {', '.join(allowed_extensions)}")
        return filetype.lower()

    def generate_unique_filename(self, realname: str, filetype: str) -> str:
        """
        Generate a unique filename
        :param realname: str
        :param filetype: str
        :return: str
        """
        sanitized_name = self.sanitize_filename(realname)
        validated_extension = self.validate_extension(filetype)
        unique_id = str(uuid.uuid4())
        return f"{sanitized_name}_{unique_id}.{validated_extension}"

    def save(self, file: File) -> File:
        """
        Save a file with sanitized name and unique id_name
        :param file: File
        :return: File
        """
    
        # Sanitize the realname
        file.realname = self.sanitize_filename(file.realname)
    
        # Generate unique id_name
        file.id_name = self.generate_unique_filename(file.realname, file.filetype)
        return repository.save(file)
    
    def update(self, file: File, id_name: str) -> File:
        """
        Update a file
        :param file: File
        :param id_name: str
        :return: File
        """
        repository.update(file, id_name)
        return file

    def delete(self, file: File) -> None:
        """
        Delete a file
        :param file: File
        """
        repository.delete(file)

    def all(self) -> List[File]:
        """
        Get all file
        :return: List[File]
        """
        return repository.all()

    def find(self, id_name: str) -> File:
        """
        Get a file by id_name
        :param id_name: str
        :return: File
        """
        return repository.find(id_name)
    