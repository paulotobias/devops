from fastapi import FastAPI # Aqui estamos importando a ferramenta FastAPI, que serve para criar a nossa API (o servidor).
from datetime import datetime ## Aqui importamos a ferramenta 'datetime', que serve para o Python entender e manipular datas e horários.

# Criamos o "coração" do nosso projeto. O APP_NOTIFICACAO é o objeto que representa a nossa aplicação web.
APP_NOTIFICACAO = FastAPI()

# Criar uma rota para receber tarefa finalizada
# APP_NOTIFICACAO.post("/notificar")
# Entrada:
#   - Recebe título da tarefa e data de finalização da tarefa
# Saída:
#   - print no terminal

# Criamos uma lista vazia chamada NOTIFICACOES. Ela vai funcionar como um "banco de dados" temporário na memória para guardar os textos das notificações.
NOTIFICACOES = []

# Esse '@' é um "decorador". Ele diz para o FastAPI: "Quando alguém acessar o endereço /notificar usando o método GET (para buscar dados), execute a função abaixo".
@APP_NOTIFICACAO.get("/notificar")
def listar_notificacoes(): # Esta função simplesmente devolve (retorna) a lista de notificações para quem pediu.
    return NOTIFICACOES

# Outro decorador. Só que este usa o método POST (usado para enviar/criar dados). Quando alguém enviar dados para /notificar, o FastAPI chama essa função.
@APP_NOTIFICACAO.post("/notificar")
def notificar(titulo: str, data_finalizacao: datetime):
    global NOTIFICACOES ## O 'global' avisa o Python que queremos mexer naquela lista NOTIFICACOES que criamos lá fora da função.
    
    # Criamos uma string formatada (f-string). Ela junta o texto com as variáveis 'titulo' e 'data_finalizacao' em uma mensagem bonita.
    resultado = f"Tarefa '{titulo}' finalizada em {data_finalizacao}"
    print(resultado) # imprime no terminal

    NOTIFICACOES.append(resultado) ## Adiciona a mensagem que acabamos de criar dentro da nossa lista de notificações.

    return {"status": "OK"} # # Responde para quem enviou a tarefa que deu tudo certo, enviando uma resposta no formato JSON.