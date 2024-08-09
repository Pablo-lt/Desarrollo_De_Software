from dataclasses import dataclass
from app import db
from datetime import datetime




@dataclass(init=False, repr=True, eq=True)
class File (db.Model):
   __tablename__= 'files'
   id_name = db.Column(db.String, primary_key=True, nullable=False)
   realname = db.Column(db.String(80), nullable=False)
   filetype = db.Column(db.String(80))
   user_id = db.Column( db.Integer, db.ForeignKey('users.id'))
   hora = db.Column(db.DateTime, nullable=False, default=datetime.now)

   user = db.relationship("User", back_populates='files', uselist=False)

   file_media = db.relationship('Media_type', back_populates='file')
