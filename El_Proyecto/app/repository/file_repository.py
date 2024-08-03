from typing import List
from app.models import File
from app import db

class FileRepository:
    """
    FileRepository class
    """

    def save(self, file: File) -> File:
        """
        Save a file
        :param file: File
        :return: File
        """
        db.session.add(file)
        db.session.commit()
        return file

    def update(self, file: File, id_name: str) -> File:
        """
        Update a file
        :param file: File
        :param id_name: str
        :return: File
        """
        entity = self.find(id_name)
        entity.realname = file.realname
        db.session.add(entity)
        db.session.commit()
        return file


    def delete(self, file: File) -> None:
        """
        Delete a file
        :param file: File
        """
        db.session.delete(file)
        db.session.commit()

    def all(self) -> List[File]:
        """
        Get all files
        :return: List[File]
        """
        return db.session.query(File).all()

    def find(self, id_name: str) -> File:
        """
        Get a file by id_name
        :param id_name: str
        :return: File
        """
        if id_name is None or id_name == 0:
            return None
        try:
            return db.session.query(File).filter(File.id_name == id_name).one()
        except:
            return None

