import os
import shutil
import subprocess
import socket


def create_skeleton():
    name_root = "app"
    # Ejecutar reflex init
    subprocess.run(["reflex", "init"], check=True)

    # Obtener el nombre del directorio actual (nombre del proyecto)
    original_name = os.path.basename(os.getcwd())

    # Reemplazar caracteres problemáticos en el nombre original
    expected_folder_name = original_name.replace("-", "_").replace(" ", "_")

    # Buscar la carpeta creada por reflex init
    created_folder_name = None
    for item in os.listdir():
        if os.path.isdir(item) and item.lower() == expected_folder_name.lower():
            created_folder_name = item
            break

    # Renombrar la carpeta encontrada
    if created_folder_name:
        os.rename(created_folder_name, name_root)

        # Actualizar el archivo rxconfig.py
        update_rxconfig_app_name(name_root)

    # Renombrar el archivo disparador de la aplicación
    for item in os.listdir():
        if os.path.isdir(item) and item.lower() == name_root:
            # Entra y buscar el archivo que concuerda con el valor de original_name + .py
            # Y lo reemplaza por el valor de expected_folder_name + .py
            for file in os.listdir(item):
                if file.lower() == f"{created_folder_name}.py":
                    os.rename(
                        os.path.join(item, file),
                        os.path.join(item, f"{name_root}.py"),
                    )
                    break
            break
    # Eliminar __pycache__
    delete_pycache()


def update_rxconfig_app_name(new_app_name):
    # Ruta del archivo rxconfig.py en la raíz del proyecto
    rxconfig_path = "rxconfig.py"

    # Verificar si el archivo existe
    if os.path.exists(rxconfig_path):
        with open(rxconfig_path, "r") as file:
            lines = file.readlines()

        # Reemplazar el valor de app_name
        with open(rxconfig_path, "w") as file:
            for line in lines:
                if "app_name=" in line:
                    line = f'    app_name="{new_app_name}",\n'
                file.write(line)


def get_free_port(default_port):
    """Intenta usar el puerto predeterminado, si está ocupado, busca otro libre."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("", default_port))
            return default_port
        except OSError:
            s.bind(("", 0))
            return s.getsockname()[1]


def run_frontend(default_port=8080):
    """Ejecuta el frontend en el puerto especificado o en uno dinámico."""
    frontend_port = get_free_port(default_port)
    subprocess.run(["reflex", "run", f"--frontend-port={frontend_port}"], check=True)


def run_backend(default_port=8000):
    """Ejecuta el backend en el puerto especificado o en uno dinámico."""
    backend_port = get_free_port(default_port)
    subprocess.run(["reflex", "run", f"--backend-port={backend_port}"], check=True)


def delete_pycache():
    # Recorrer el árbol de directorios y eliminar __pycache__
    for root, dirs, files in os.walk("."):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                pycache_path = os.path.join(root, dir_name)
                shutil.rmtree(pycache_path)
