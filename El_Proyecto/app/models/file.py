from dataclasses import dataclass
from app import db
import uuid
from datetime import datetime


def generate_unique_filename(extension="txt"):
   unique_id=uuid.uuid4()
   unique_name=f"{unique_id}.{extension}"
   return unique_name

@dataclass(init=False, repr=True, eq=True)
class File (db.Model):
   __tablename__= 'files'
   id_name = db.Column(db.String, primary_key=True, nullable=False, default=generate_unique_filename)
   realname = db.Column(db.String(80), nullable=False)
   filetype = db.Column(db.String(80))
   user_id = db.Column( db.Integer, db.ForeignKey('users.id'))
   hora: datetime = db.Column(db.DateTime, nullable=False, default=datetime.now)

   user = db.relationship("User", back_populates='files', uselist=False)

   file_media = db.relationship('Media_type', back_populates='file')
