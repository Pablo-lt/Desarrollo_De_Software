import os
import shutil
import magic
from dataclasses import dataclass
from app import db
from datetime import datetime
from sqlalchemy import func

@dataclass(init=False, repr=True, eq=True)
class File(db.Model):
    __tablename__ = 'files'
    id_name = db.Column(db.String, primary_key=True, nullable=False)
    realname = db.Column(db.String(80), nullable=False)
    filetype = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    hora = db.Column(db.DateTime, nullable=False, server_default=func.now())

    user = db.relationship("User", back_populates='files', uselist=False)
    file_media = db.relationship('Media_type', back_populates='file')

    @staticmethod
    def identify_file_type(file_path):
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(file_path)
        
        if file_type.startswith('audio'):
            return 'audio'
        elif file_type.startswith('video'):
            return 'video'
        elif file_type.startswith('image'):
            return 'imagen'
        else:
            return 'desconocido'

    @staticmethod
    def move_file(file_path, base_directory):
        tipo = File.identify_file_type(file_path)
        if tipo != 'desconocido':
            destino = os.path.join(base_directory, tipo)
            os.makedirs(destino, exist_ok=True)
            shutil.move(file_path, destino)
            print(f'{file_path} movido a {destino}')
            return destino
        else:
            print(f'No se pudo identificar el tipo de {file_path}')
            return None

    @staticmethod
    def process_files(input_directory, base_directory):
        for root, _, files in os.walk(input_directory):
            for file in files:
                file_path = os.path.join(root, file)
                new_path = File.move_file(file_path, base_directory)
                if new_path:
                    new_file = File(
                        id_name=os.path.basename(new_path),
                        realname=file,
                        filetype=os.path.splitext(file)[1],
                    )
                    db.session.add(new_file)
        db.session.commit()

def main():
    input_directory = input("Por favor, ingrese la ruta del directorio de entrada: ")
    base_directory = 'C:\\Users\\enzon\\VSC\\Desarrollo-De-Software\\Proyecto\\uploads'
    
    if not os.path.isdir(input_directory):
        print(f"El directorio de entrada '{input_directory}' no existe.")
        return
    
    if not os.path.isdir(base_directory):
        print(f"El directorio base '{base_directory}' no existe.")
        return
    
    File.process_files(input_directory, base_directory)

if __name__ == "__main__":
    main()