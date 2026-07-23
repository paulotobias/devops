# devops
1. Descrição da Aplicação
Essa é uma aplicação API REST com armazenamento em tempo de execução utilizando FastAPI

2. Instrução para execução Local
Passos.
    Instalação do Vmware e import da Iso utilizada contendo aplicação kind para uso do kubernetes
    Fazer o pull do projeto: https://github.com/paulotobias/devops.git
    Iniciar o Deployment com o comando kubectl apply -f deployment.yaml nos próximos as atualizações serão executadas via push e merge no github
    Obter o endereço da VM que hospeda o ambiente e fazer um port forward com o comando:  kubectl port-forward --address 0.0.0.0 svc/devops-svc 30005:8000
    Acessar o navegador no endereço e porta porta 30005

3. tecnologias utilizadas
Linguagem e Framework:
    Python: Linguagem principal utilizada para o desenvolvimento da aplicação.
    FastAPI: Framework web moderno e de alto desempenho para a criação das APIs.

Containerização e Orquestração:
    Docker: Utilizado para a criação de imagens e empacotamento da aplicação e suas dependências.
    Kubernetes (kind): Kubernetes in Docker utilizado para a orquestração dos contêineres e gerenciamento dos pods no ambiente local/de testes.

Integração e Entrega Contínua (CI/CD):
    GitHub: Controle de versão do código fonte e repositório remoto.
    GitHub Actions Runner (Gitrunner): Agente de execução responsável por rodar as rotinas automatizadas do pipeline de CI/CD.

Infraestrutura e Sistema Operacional:
    Linux (Ubuntu / Debian): Sistema operacional utilizado no ambiente de execução do runner e dos nós do cluster.
    VMware Workstation: Hipervisor de virtualização utilizado para provisionar a máquina virtual que hospeda o ambiente de desenvolvimento e o cluster.
