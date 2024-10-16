# API Proyecto GIP

## Pasos para levantar el proyecto

1. Tener python instalado
2. Recomendablemente, usar un virtual env ([documentación oficial](https://fastapi.tiangolo.com/virtual-environments/))
    1. Ejecutar el comando `.venv\Scripts\Activate.ps1` en una terminal estando sobre la ruta del proyecto
    2. Validar que esté activo el entorno virtual `Get-Command python`
    3. Actualizar pip `python -m pip install --upgrade pip`
3. Instalar dependencias con `pip install -r requirements.txt`
4. Levantar el API con `uvicorn main:app --reload`


### Variables de entorno

Necesario configurar las siguientes variables, para una correcta ejecución: 

Tanto la URL como la KEY del API, son proveidas por Supabase:
export SUPABASE_URL="my-url-to-my-awesome-supabase-instance"
export SUPABASE_KEY="my-supa-dupa-secret-supabase-api-key"


## Pasos para probar la aplicación desde local

1. Instalar Postman o algún otro programa que te permita hacer peticiones (otra alternativa es Insomnia)
2. Colocar que se va a crear una nueva petición de tipo POST a la siguiente ruta: `http://localhost:8000/data-upload`
3. Configurar el body de la petición para que sea de tipo Form multi-part
4. Agregar una entrada del body llamada "rips" y a esta adjuntarle uno de los reportes de los meses de rips que se
   enviaron por wpp
5. Agregar una entrada del body llamada "monthly" y a este adjuntarle el equivalente pero del archivo que se llama "
   informe..."
6. Enviar la petición

