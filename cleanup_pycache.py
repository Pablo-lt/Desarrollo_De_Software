import os
import shutil

def eliminar_pycache(directorio):
    """Elimina todas las carpetas __pycache__ dentro del directorio dado."""
    for root, dirs, _ in os.walk(directorio, topdown=False):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                pycache_path = os.path.join(root, dir_name)
                print(f'Eliminando carpeta: {pycache_path}')
                shutil.rmtree(pycache_path)

def main():
    """Función principal para eliminar carpetas __pycache__."""
    directorio_base = 'Proyecto'  # Ajusta aquí el nombre de la carpeta principal
    if not os.path.isdir(directorio_base):
        print(f"El directorio '{directorio_base}' no existe.")
        return
    eliminar_pycache(directorio_base)

if __name__ == "__main__":
    main()
