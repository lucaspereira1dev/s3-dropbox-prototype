from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import bucket_helpers  # módulo já adaptado para GCP Storage
import os

load_dotenv()  # Carrega variáveis do .env

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Necessário para flash messages

def get_file_type(filename):
    ext = filename.split('.')[-1].upper()
    if ext:
        return ext
    else:
        return "ARQUIVO"

# Rota Principal: Dashboard
@app.route('/')
def index():
    files = bucket_helpers.list_files()
    files_with_type = [(f, get_file_type(f)) for f in files]
    return render_template('index.html', files=files_with_type)

# Rota para Upload
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('Nenhum arquivo selecionado')
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash('Nenhum arquivo selecionado')
        return redirect(url_for('index'))

    if file:
        # Usa o nome original do arquivo
        filename = file.filename

        if bucket_helpers.upload_file(file, filename):
            flash(f'Arquivo "{filename}" enviado com sucesso!')
        else:
            flash(f'Erro ao enviar o arquivo "{filename}".')

    return redirect(url_for('index'))

# Rota para Download
@app.route('/download/<filename>')
def download(filename):
    url = bucket_helpers.get_download_url(filename)
    if url:
        # Redireciona para o link assinado do GCP Storage
        return redirect(url)
    else:
        flash('Erro ao gerar link de download.')
        return redirect(url_for('index'))

# Rota para Deletar
@app.route('/delete/<filename>')
def delete(filename):
    if bucket_helpers.delete_file(filename):
        flash(f'Arquivo "{filename}" deletado com sucesso!')
    else:
        flash(f'Erro ao deletar o arquivo "{filename}".')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=9090)
