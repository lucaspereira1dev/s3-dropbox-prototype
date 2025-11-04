from google.cloud import storage
import os
from dotenv import load_dotenv

load_dotenv()

# Nome do bucket, armazenado como variável de ambiente GCS_BUCKET_NAME
GCS_BUCKET_NAME = os.environ.get('GCS_BUCKET_NAME')

# Inicialize o cliente Storage usando credenciais padrão (GOOGLE_APPLICATION_CREDENTIALS)
storage_client = storage.Client()

def list_files():
    """Lista os arquivos no bucket GCS"""
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    return [blob.name for blob in bucket.list_blobs()]

def upload_file(file_obj, filename):
    """Faz upload de um arquivo para o GCS"""
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_file(file_obj)
    return True

def get_download_url(filename):
    """Gera uma URL assinada para download"""
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(filename)
    url = blob.generate_signed_url(version="v4", expiration=3600, method="GET")
    return url

def delete_file(filename):
    """Deleta um arquivo do GCS"""
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.delete()
    return True
