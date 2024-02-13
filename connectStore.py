from flask import Flask

app = Flask(__name__) # inicializa o Flask e associa o projeto atual a ele
app.config.from_pyfile('config.py') # referencia o arquivo de conexao e o proprio python consegue buscar as variaveis do arquivo automaticamente

from controller.usuarioController import *
from controller.consoleController import *
from controller.categoriaController import *
from controller.jogoController import *

# define esse arquivo como sendo a main do projeto
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)