import uuid
from typing import List
from app.models import file
from app.repository import FileRepository
import magic
import os
import shutil
repository = FileRepository()

class FileService:
    def __init__(self):
        pass

    def sanitize_filename(self, filename: str) -> str:
        # Compara creando el nombre en limpio encadenando caracteres alfanumericos y de "-" o "_", invalidando cualquier otro caracter.
        sanitized = ''.join(c for c in filename if c.isalnum() or c in ('-', '_')).lower()
        if sanitized != filename.lower():
            raise ValueError("El nombre del archivo solo puede contener caracteres alfanuméricos, guiones y guiones bajos.")
        return sanitized

    def extension_type(file_path):
        # Permite identificar el tipo de archivo mediante la libreria python-magic.
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(file_path)
        if file_type.startswith('audio'):
            return 'audio'
        elif file_type.startswith('video'):
            return 'video'
        elif file_type.startswith('image'):
            return 'imagen'
        elif  file_type.startswith('pdf'):
            return 'PDF Document'
        elif file_type.startswith('msword'):
            return 'Word Document (.doc)'
        elif file_type.startswith('vnd.openxmlformats-officedocument.wordprocessingml.document'):
            return 'Word Document (.docx)'
        # Cualquier otro tipo no definido se establecera como desconocido.
        else:
            return 'desconocido'

    def generate_unique_filename(self, realname: str, filetype: str) -> str:
        # genera un nombre unico para el archivo mediante el nombre en limpio anterior y el uuid4.
        sanitized_name = self.sanitize_filename(realname)
        validated_extension = self.validate_extension(filetype)
        unique_id = str(uuid.uuid4())
        return f"{sanitized_name}_{unique_id}.{validated_extension}"

    def save(self, file: file) -> file:
        # Guarda el nombre en limpio con su uuid en el directorio "repository".
        file.realname = self.sanitize_filename(file.realname)
        file.id_name = self.generate_unique_filename(file.realname, file.filetype)
        return repository.save(file)
    
    def update(self, file: file, id_name: str) -> file:
        # Actualizamos los datos en el archivo.
        repository.update(file, id_name)
        return file

    def delete(self, File: file) -> None:
        # Funcion para eliminar un archivo.
        repository.delete(file)

    def find(self, id_name: str) -> file:
        # Funcion para encontrar un archivo.
        return repository.find(id_name)

    def mover_archivo(self, file_path, base_directory):
        # Funcion para mover un archivo del directorio en el que se encuentre a otro directorio destino.
        tipo = self.extension_type(file_path)
        if tipo != 'desconocido':
            # Si el archivo no tiene problemas, establecemos el directorio destino.
            destino = os.path.join(base_directory, tipo)
            os.makedirs(destino, exist_ok=True)
            shutil.move(file_path, destino)
            print(f'{file_path} movido a {destino}')
        else:   #caso contrario
            print(f'No se pudo identificar el tipo de {file_path}')

    def procesar_archivos(self, directorio_entrada, base_directory):
        # Procesamiento para mover los archivos desde el directorio de entrada al de destino.
        for root, _, files in os.walk(directorio_entrada):
            for file in files:
                file_path = os.path.join(root, file)
                self.mover_archivo(file_path, base_directory)

    def main(self):
        # Aqui definimos cuales son los directorios entrada y destino, ejecutando finalmente la funcion "procesar_archivos".
        directorio_entrada = input("Por favor, ingrese la ruta del directorio de entrada: ")
        base_directory = input("Por favor, ingrese la ruta del directorio base de destino: ")
        if not os.path.isdir(directorio_entrada):
            print(f"El directorio de entrada '{directorio_entrada}' no existe.")
            return
        if not os.path.isdir(base_directory):
            print(f"El directorio base '{base_directory}' no existe.")
            return
        self.procesar_archivos(directorio_entrada, base_directory)
    if __name__ == "__main__":
        main()
