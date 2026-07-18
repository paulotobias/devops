from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from datetime import datetime
import requests
import logging
import os

level = os.environ.get("LOG_LEVEL", logging.INFO)

if level == "DEBUG":
    level = logging.DEBUG
else:
    level = logging.INFO

LISTA_TAREFAS = []
APP = FastAPI()

LOGGER = logging.getLogger("devops")
LOGGER.setLevel(level)

stream_handler = logging.StreamHandler()
file_handler   = logging.FileHandler("api.log", encoding='utf-8')
formatador     = logging.Formatter(fmt="%(name)s | %(asctime)s | %(filename)s:%(lineno)s | %(levelname)s | %(message)s")

stream_handler.setFormatter(formatador)
file_handler.setFormatter(formatador)
LOGGER.addHandler(stream_handler)
LOGGER.addHandler(file_handler)

# IMPORTANTE: Importa a biblioteca 'requests', que serve para fazer requisições HTTP.
# É ela quem vai permitir que este código "ligue" e converse com o outro código (App de Notificação).

METRICAS = {
    'qtde_tarefas': 0,
    'qtde_tarefas_pendentes': 0,
    'qtde_tarefas_concluidas': 0,
    'qtde_tarefas_atualizadas': 0,
    'qtde_tarefas_removidas': 0,
    'qtde_tarefas_removidas': 0,
    'tempo_medio_conclusao_tarefas': 0

}

##Funções 
def nova_tarefa(id: int, titulo: str, descricao: str):
    return {
        "id": id,
        "titulo": titulo,
        "descricao": descricao,
        "concluido": False,
        "criado_em": datetime.now()
    }
    LOGGER.debug(f"Criando tarefa='{str(tarefa)}'")

    return tarefa

def verificar_existencia_tarefa(id: int):
    for tarefa in LISTA_TAREFAS:
        if id == tarefa['id']:
            return True
    return False

#Rotas
@APP.get("/")
def index():
    LOGGER.info(f"Rota '/' foi acessada")
    return "Olá, DevOps!"

@APP.get("/tarefas")
def listar_tarefas():
    # Lista tarefas (somente id e titulo)
    LOGGER.info(f"Rota '/tarefas' foi acessada")
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
        LOGGER.error(f"Rota '/tarefas/{id} acessada. Mensagem: {mensagem_padrao['mensagem']}")
        return mensagem_padrao
    
    # ID da tarefa é o índice na lista
    if id >= 0 and id < len(LISTA_TAREFAS):
        LOGGER.info(f"Rota '/tarefas/{id} acessada.")
        return LISTA_TAREFAS[id]
    
    return mensagem_padrao

@APP.post("/tarefas", status_code=201)
def criar_tarefa(id: int, titulo: str, descricao: str):
    global LISTA_TAREFAS

    tarefa_existe = verificar_existencia_tarefa(id)

    if tarefa_existe:
        ex = HTTPException(status_code=202, detail={"mensagem": "TAREFA JÁ EXISTE!"})
        LOGGER.error(f"Rota POST '/tarefas/' acessada. Tarefa já existe.")
        raise ex
    
    nova = nova_tarefa(id, titulo, descricao)

    LISTA_TAREFAS.append(nova)

    LOGGER.info(f"Rota POST '/tarefas' acessada. Tarefa id={id} criada.")

    return {"mensagem": "OK"}

@APP.put("/tarefas/{id}")
def atualizar_tarefa(id: int, titulo: str = "", descricao: str = "", concluido: bool = False):
    global LISTA_TAREFAS

    tarefa_existe = verificar_existencia_tarefa(id)

    if not tarefa_existe:
        LOGGER.error(f"Rota PUT '/tarefas/{id}' acessada. Tarefa NÃO existe.")
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
        requests.post(f"http://notificacoes:8000/notificar?titulo={tarefa['titulo']}&data_finalizacao={datetime.now()}", timeout=10)

    LISTA_TAREFAS[indice]['concluido'] = concluido
    LOGGER.debug(f"Tarefa atualizada = {LISTA_TAREFAS[indice]}")
    LOGGER.info(f"Rota PUT '/tarefas/{id}' acessada. Tarefa id={id} atualizada.")

    return {"mensagem": "OK"}

@APP.delete("/tarefas/{id}")
def apagar_tarefa(id: int):
    global LISTA_TAREFAS

    tarefa_existe = verificar_existencia_tarefa(id)

    if not tarefa_existe:
        LOGGER.error(f"Rota PUT '/tarefas/{id}' acessada. Tarefa NÃO existe.")
        return {"mensagem": "TAREFA NÃO EXISTE"}

    tarefa = None
    for indice in range(len(LISTA_TAREFAS)):
        tarefa = LISTA_TAREFAS[indice]

        # Sai do loop
        if tarefa['id'] == id:
            break
    
    LISTA_TAREFAS.pop(indice)

    LOGGER.info(f"Rota DELETE '/tarefas/{id}' acessada. Tarefa id={id} removida.")

    return {"mensagem": "OK"}

@APP.get("/health", status_code=200)
def health_check():
    return {"status": "OK"}