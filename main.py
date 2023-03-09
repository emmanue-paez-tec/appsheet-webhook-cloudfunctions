from urllib.parse import urlparse, parse_qs
from google.cloud import storage
import requests


def leer_documento(request):

    request_json = request.get_json()
    if request_json and 'row_id' in request_json and 'titulo' in request_json:
        print(request_json['row_id'])
        print(request_json['titulo'])
        print(request_json['path'])
        
        #extraer path
        parsed_url = urlparse(request_json['path'])
        params =dict( parse_qs(parsed_url.query))
        print(params)

        #leer de cloud Storage
        storage_client=storage.Client()
        bucket = storage_client.bucket("Bucket")
        blob = bucket.blob("appsheet/data/Nombre de la App/"+params["fileName"][0])
        filetext=""
        with blob.open("r") as f:
            filetext=f.read()
            print(filetext)
        
        ## TODO, transformar texto del documento

        #Escribir a Appsheet API 
        appId="APP ID"
        applicationAccessKey="Acess key"
        tableName="Tareas"

        url = f'https://api.appsheet.com/api/v2/apps/{appId}/tables/{tableName}/Action?applicationAccessKey={applicationAccessKey}'
        payload = {
            "Action":"Edit",
            "Properties":{},
            "Rows":[
                {
                    "Titulo":request_json['titulo'],
                    "Row ID":request_json['row_id'],
                    "Texto_entregable":filetext
                }
            ]
        }
        response = requests.post(url,json=payload)
        print(response.text)

        return "ok!"
    else:
        return "error!"
