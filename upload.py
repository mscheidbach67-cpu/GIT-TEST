import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Récupération des secrets
creds_json = json.loads(os.environ["GDRIVE_CREDENTIALS"])
folder_id  = os.environ["GDRIVE_FOLDER_ID"]

# Connexion à l'API Drive
creds   = Credentials.from_service_account_info(creds_json, scopes=["https://www.googleapis.com/auth/drive"])
service = build("drive", "v3", credentials=creds)

# Chercher si le fichier existe déjà dans Drive
results = service.files().list(
    q=f"name='document.txt' and '{folder_id}' in parents and trashed=false",
    fields="files(id, name)"
).execute()
files = results.get("files", [])

media = MediaFileUpload("document.txt", mimetype="text/plain", resumable=True)

if files:
    # Mise à jour du fichier existant
    file_id = files[0]["id"]
    service.files().update(fileId=file_id, media_body=media).execute()
    print(f"Fichier mis à jour (id: {file_id})")
else:
    # Création du fichier
    metadata = {"name": "document.txt", "parents": [folder_id]}
    service.files().create(body=metadata, media_body=media, fields="id").execute()
    print("Fichier créé dans Drive")
