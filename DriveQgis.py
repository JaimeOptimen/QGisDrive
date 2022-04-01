#Imports Necesarios
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.files import FileNotUploadedError
import os
#Archivo de credenciales
directorio_credenciales = 'credentials_module.json'

#Autenticación en Drive
def login():
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = directorio_credenciales
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)
    
    if gauth.credentials is None:
        gauth.LocalWebserverAuth(port_numbers=[8092])
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
        
    gauth.SaveCredentialsFile(directorio_credenciales)
    credenciales = GoogleDrive(gauth)
    return credenciales


#Función para subir archivo
def subir_archivo(ruta_archivo,id_folder,filename):
    credenciales = login()
    archivo = credenciales.CreateFile({'parents': [{"kind": "drive#fileLink",\
                                                    "id": id_folder}]})
    archivo['title'] = filename
    archivo.SetContentFile(ruta_archivo)
    archivo.Upload()

#Funcion principal
if __name__ == "__main__":
    ruta_archivo = 'D:/grovision/'
    id_folder = 'ID DE TU FOLDER'
    #Recorrer y buscar archivos con terminaciones 
    for filename in os.listdir(ruta_archivo):
        if filename.endswith(".shp") or filename.endswith(".gpkg") or filename.endswith(".shx") or filename.endswith(".dbf") or filename.endswith(".prj") or filename.endswith(".sdat") or filename.endswith(".sgrd") or filename.endswith(".module") or filename.endswith(".cpg") or filename.endswith(".tif") or filename.endswith(".gpkg-shm") or filename.endswith(".gpkg-wal") or filename.endswith(".xml"):
            print(os.path.join(ruta_archivo,filename))
            subir_archivo(ruta_archivo + filename,id_folder,filename)

    