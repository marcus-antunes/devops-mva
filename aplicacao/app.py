from flask import Flask, render_template
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

class BaseModel(DeclarativeBase): pass
CAMINHO_BD = "sqlite:///banco.db"
BD = SQLAlchemy(model_class=BaseModel)
APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = CAMINHO_BD
BD.init_app(APP)

migrate = Migrate(APP, BD)

class Livro(BD.Model):
    __tablename__ = 'livro'
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str]
    autor: Mapped[str]
    issn: Mapped[str]
    data_publicacao: Mapped[datetime]
    #qtde_paginas: Mapped[int] = mapped_column()
    qtde_paginas: Mapped[int]  # ✅ Adicionado ':'

    def get_titulo(self):
        return self.titulo

@APP.route("/")
def index():
    return render_template('index.html')

@APP.route("/livros", methods=['GET', 'POST'])
def livros():
    
    #if Livro.query.count() == 0:
    #    BD.session.add(Livro(
    #        titulo="1984",
    #        autor="George Orwell",
    #        issn="1234",
    #        data_publicacao=datetime.now(),
    #        qtde_paginas=320
    #    ))
    #    BD.session.commit()
    
    livros = Livro.query.all()
    return render_template('livros.html', livros=livros)

@APP.route("/criar_livro", methods=['POST'])
def criar_livro():
    req = request.get_json()
    print (req)
    livro = Livro(
        titulo=req['titulo'],
        autor=req['autor'],
        data_publicacao=datetime.now(),
        qtde_paginas=0,
        issn=""
        )
    BD.session.add(livro)
    BD.session.commit()
    return "Livro criado com Sucesso!"




if __name__ == '__main__':
    with APP.app_context():
        BD.create_all()

        livro = Livro(
            titulo = "1984",
            autor= "George Orwell",
            data_publicacao = datetime.now(),
            qtde_paginas = 320,
            issn = "1234"
        )
        BD.session.add(livro)
        BD.session.commit()

        BD.session.add(Livro(
            id = 3,
            titulo = "Sentido da Vida",
            autor= "Viktor Frankl",
            data_publicacao = datetime.now(),
            qtde_paginas = 120,
            issn = "4321"
        ))
        BD.session.commit()


    APP.run(debug=True)