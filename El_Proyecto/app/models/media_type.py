from dataclasses import dataclass
from app import db

@dataclass(init=False, repr=True, eq=True)
class Media_type(db.Model):
    __tablename__ = 'media_type'

    file_id = db.Column(db.String, db.ForeignKey('files.id_name'),primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    size = db.Column(db.Integer, nullable=False)

    file= db.relationship('File', back_populates='file_media')
