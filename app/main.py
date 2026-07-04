from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from datetime import datetime

# IMPORTANTE: Importa a biblioteca 'requests', que serve para fazer requisições HTTP.
# É ela quem vai permitir que este código "ligue" e converse com o outro código (App de Notificação).
import requests

LISTA_TAREFAS = []
APP = FastAPI()
##Funções 
def nova_tarefa(id: int, titulo: str, descricao: str):
    return {
        "id": id,
        "titulo": titulo,
        "descricao": descricao,
        "concluido": False,
        "criado_em": datetime.now()
    }

def verificar_existencia_tarefa(id: int):
    for tarefa in LISTA_TAREFAS:
        if id == tarefa['id']:
            return True
    return False

#Rotas
@APP.get("/")
def index():
    return "Olá, DevOps!"

@APP.get("/tarefas")
def listar_tarefas():
    # Lista tarefas (somente id e titulo)
    if len(LISTA_TAREFAS) == 0:
        return LISTA_TAREFAS

    tarefas = []
    
    for tarefa in LISTA_TAREFAS:
        info = {"id": tarefa['id'], "titulo": tarefa['titulo']}
        tarefas.append(info)

    return tarefas

@APP.get("/tarefas/{id}")
def listar_tarefa_especifica(id: int):
    mensagem_padrao = {"mensagem": "Não existe nenhuma tarefa"}
    if len(LISTA_TAREFAS) == 0:
        return mensagem_padrao
    
    # ID da tarefa é o índice na lista
    if id >= 0 and id < len(LISTA_TAREFAS):
        return LISTA_TAREFAS[id]
    
    return mensagem_padrao

@APP.post("/tarefas, status_code=201")
def criar_tarefa(id: int, titulo: str, descricao: str):
    global LISTA_TAREFAS

    tarefa_existe = verificar_existencia_tarefa(id)

    if tarefa_existe:
        ex = HTTPException(status_code=202, detail={"mensagem": "TAREFA JÁ EXISTE!"})
        raise ex
    
    nova = nova_tarefa(id, titulo, descricao)

    LISTA_TAREFAS.append(nova)

    return {"mensagem": "OK"}

@APP.put("/tarefas/{id}")
def atualizar_tarefa(id: int, titulo: str = "", descricao: str = "", concluido: bool = False):
    global LISTA_TAREFAS

    tarefa_existe = verificar_existencia_tarefa(id)

    if not tarefa_existe:
        return {"mensagem": "TAREFA NÃO EXISTE!"}
    
    tarefa = None
    for indice in range(len(LISTA_TAREFAS)):
        tarefa = LISTA_TAREFAS[indice]

        # Sai do loop
        if tarefa['id'] == id:
            break
    
    if titulo != "":
        LISTA_TAREFAS[indice]['titulo'] = titulo
    
    if descricao !=  "": 
        LISTA_TAREFAS[indice]['descricao'] = descricao
    
    if concluido == True:
        requests.post(f"http://localhost:8002/notificar?titulo={tarefa['titulo']}&data_finalizacao={datetime.now()}")

    LISTA_TAREFAS[indice]['concluido'] = concluido

    return {"mensagem": "OK"}

@APP.delete("/tarefas/{id}")
def apagar_tarefa(id: int):
    global LISTA_TAREFAS

    tarefa_existe = verificar_existencia_tarefa(id)

    if not tarefa_existe:
        return {"mensagem": "TAREFA NÃO EXISTE"}

    tarefa = None
    for indice in range(len(LISTA_TAREFAS)):
        tarefa = LISTA_TAREFAS[indice]

        # Sai do loop
        if tarefa['id'] == id:
            break
    
    LISTA_TAREFAS.pop(indice)

    return {"mensagem": "OK"}