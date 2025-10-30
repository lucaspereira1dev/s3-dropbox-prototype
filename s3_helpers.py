import boto3
import os
from botocore.exceptions import ClientError

# Carregamos o nome do bucket do .env
S3_BUCKET = os.environ.get('S3_BUCKET_NAME')
s3_client = boto3.client('s3')

def list_files():
    """Lista os arquivos no bucket S3"""
    try:
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET)
    except ClientError as e:
        print(f"Erro ao listar arquivos: {e}")
        return []
    
    files = response.get('Contents', [])
    return files

def upload_file(file_obj, filename):
    """Faz upload de um arquivo para o S3"""
    try:
        s3_client.upload_fileobj(
            file_obj,
            S3_BUCKET,
            filename,
            ExtraArgs={'ContentType': file_obj.content_type} # Importante para o navegador!
        )
    except ClientError as e:
        print(f"Erro no upload: {e}")
        return False
    return True

def get_download_url(filename):
    """
    Gera uma URL pré-assinada para download.
    Esta é a forma correta e segura! Não fazemos proxy do download.
    O usuário baixa DIRETAMENTE do S3.
    """
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET, 'Key': filename},
            ExpiresIn=3600  # URL expira em 1 hora
        )
    except ClientError as e:
        print(f"Erro ao gerar URL: {e}")
        return None
    return url

def delete_file(filename):
    """Deleta um arquivo do S3"""
    try:
        s3_client.delete_object(Bucket=S3_BUCKET, Key=filename)
    except ClientError as e:
        print(f"Erro ao deletar: {e}")
        return False
    return True