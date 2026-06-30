import pytest
from datetime import datetime
from app import APP,BD,Livro

#@pytest.fixture()
#def client():
#    app = APP
#    app.config.update({
#        "TESTING": True
#    })

#    yield app.test_client()

#def test_index(client):
#    resposta = client.get("/")
#    conteudo_da_resposta = resposta.text
#    conteudo_esperado = """<h1>Integrantes</h1>
#
#<br>
#Marcus Antunes"""
#    assert conteudo_esperado == conteudo_da_resposta


@pytest.fixture
def client():
    APP.config['TESTING'] = True
    with APP.test_client() as client:
        with APP.app_context():
            BD.create_all()
            # Insere um livro de teste
            livro = Livro(
                titulo="1984",
                autor="George Orwell",
                issn="1234",
                data_publicacao=datetime.now(),
                qtde_paginas=320
            )
            BD.session.add(livro)
            BD.session.commit()
        yield client
        with APP.app_context():
            BD.drop_all()

def test_livros(client):
    resposta = client.get("/livros")
    assert resposta.status_code == 200
    assert "1984" in resposta.text  # Verifica se o título está no HTML