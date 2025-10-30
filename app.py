from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import s3_helpers # Nosso módulo
import os

load_dotenv() # Carrega as variáveis do .env

app = Flask(__name__)
app.secret_key = os.urandom(24) # Necessário para 'flash messages'

# Rota Principal: Dashboard
@app.route('/')
def index():
    files = s3_helpers.list_files()
    return render_template('index.html', files=files)

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
        # Usamos o nome original do arquivo
        filename = file.filename
        
        if s3_helpers.upload_file(file, filename):
            flash(f'Arquivo "{filename}" enviado com sucesso!')
        else:
            flash(f'Erro ao enviar o arquivo "{filename}".')
            
    return redirect(url_for('index'))

# Rota para Download
@app.route('/download/<filename>')
def download(filename):
    url = s3_helpers.get_download_url(filename)
    if url:
        # Redireciona o navegador do usuário para a URL do S3
        return redirect(url)
    else:
        flash('Erro ao gerar link de download.')
        return redirect(url_for('index'))

# Rota para Deletar
@app.route('/delete/<filename>')
def delete(filename):
    if s3_helpers.delete_file(filename):
        flash(f'Arquivo "{filename}" deletado com sucesso!')
    else:
        flash(f'Erro ao deletar o arquivo "{filename}".')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=9090)