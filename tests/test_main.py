# def soma(a, b):
#     return 8

# def test_soma_positivos():
#     assert soma(4, 4) == 8

# def test_soma_errada():
#     assert soma(3, 7) == 10
from fastapi.testclient import TestClient
from app import APP


CLIENT = TestClient(APP)

def test_index():
    requisicao = CLIENT.get("/")
    assert requisicao.status_code == 200
    


def test_put():
    requisicao = CLIENT.post("/tarefas?id=0&titulo=tarefa&descricao=descricao")
    assert requisicao.status_code == 201
    assert requisicao.json() == {"mensagem": "OK"} 

    requisicao = CLIENT.post("/tarefas?id=0&titulo=tarefa&descricao=descricao")
    assert requisicao.status_code == 202
    assert requisicao.json()['detail'] == {"mensagem": "TAREFA JÁ EXISTE!"}