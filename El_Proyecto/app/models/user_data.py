from dataclasses import dataclass
from app import db

@dataclass(init=False, repr=True, eq=True)
class UserData(db.Model):
    __tablename__ = 'users_data'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname: str = db.Column(db.String(80), nullable=False)
    lastname: str = db.Column(db.String(80), nullable=False)
    phone: str = db.Column(db.String(120), nullable=False)
    description: str = db.Column(db.String(500), nullable=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    #Relacion Uno a Uno bidireccional con User
    #Flask Web Development Capitulo: Database Relationships Revisited Pag 49,149 
    user = db.relationship("User", back_populates='data', uselist=False)
    