import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory, jsonify

app = Flask(__name__)
# UPLOAD_FOLDER = './data'
UPLOAD_FOLDER = r'T:\CLIENTES\GRUPO VISAN\INTEGRACAO\ARQUIVOS BENNER'
UPLOAD_FOLDER_ALTER = r'C:\Users\VM100\Documents\RepositorioGit\visanAPI\data'

ALLOWED_EXTENSIONS = {'zip'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_ALTER'] = UPLOAD_FOLDER_ALTER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/visan', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        
        # verifique se a solicitacao de postagem tem a parte do arquivo
        if 'file' not in request.files:
            flash('Nao tem a parte do arquivo')
            return redirect(request.url)
        file = request.files['file']
        
        # Se o usuario nao selecionar um arquivo, o navegador envia um
        # arquivo vazio sem um nome de arquivo.
        
        if file.filename == '':
            flash('Nenhum arquivo selecionado')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            try:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return "arquivo salvo com sucesso"
            except:
                file.save(os.path.join(app.config['UPLOAD_FOLDER_ALTER'], filename))
                return "arquivo salvo na pasta data"
            # return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <html>
    <head>
        <title>Upload File</title>
    </head>
    <body>
        <h1>File Upload</h1>
        <form method="POST" action="" enctype="multipart/form-data">
        <p><input type="file" name="file"></p>
        <p><input type="submit" value="Submit"></p>
        </form>
    </body>
    </html>
        '''
    
    
@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


if __name__ == '__main__':
    app.run(host="192.168.75.114", port=80, debug = True)
    # host="192.168.75.114"
