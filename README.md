# Instrumentos B3 - FastAPI
Esta é uma API de alta performance desenvolvida em Python com o framework FastAPI. Sua principal finalidade é receber e processar os arquivos **InstrumentsConsolidatedFile da B3** (nos formatos CSV e Excel), realizando a leitura de forma assíncrona em segundo plano e disponibilizando os dados extraídos para consulta através de endpoints seguros.
O sistema foi projetado para ser robusto e escalável, utilizando uma arquitetura baseada em contêineres e uma fila de processamento para lidar com arquivos grandes sem bloquear a resposta ao usuário.

## Tecnologias
A aplicação utiliza um conjunto de tecnologias para garantir performance e eficiência:
- **FastAPI:** Framework web Python de alta performance para a construção da API.
- **MongoDB:** Banco de dados NoSQL utilizado para armazenar o histórico de uploads e os dados extraídos dos arquivos.
- **Celery:** Sistema de fila de tarefas distribuídas, responsável por executar o processamento pesado dos arquivos em background, sem travar a API.
- **Redis:** Utilizado para duas finalidades críticas:
  - **Message Broker:** Gerencia a comunicação e a fila de tarefas entre a API e os workers Celery.
  - **Cache:** Armazena temporariamente os resultados de consultas frequentes, acelerando drasticamente as respostas do endpoint de busca de conteúdo.
- **Docker & Docker Compose:** A aplicação é totalmente containerizada, garantindo um ambiente de desenvolvimento e produção consistente e isolado. O Docker Compose orquestra todos os serviços (API, worker, banco de dados e cache) com um único comando.

## Como executar o projeto
Para executar a aplicação em seu ambiente local, siga os passos abaixo.

**Pré-requisito**
- Docker instalado.


**Passos para Execução**
1. Clone este repositório para a sua máquina.
2. Crie o arquivo de ambiente:
  - Na raiz do projeto, crie um arquivo chamado `.env` e copie o conteúdo do arquivo `.env.example`. Este arquivo contém as senhas e chaves necessárias para a aplicação.
3. Inicie os contêineres:
  - Abra um terminal na pasta raiz do projeto e execute o seguinte comando:

    `docker-compose up --build`

## Acessando a documentação
Após a inicialização, a API estará disponível em `http://localhost:8000.`.
Para acessar a documentação interativa (Swagger UI), onde você pode visualizar e testar todos os endpoints, acesse o seguinte endereço no seu navegador:

`http://localhost:8000/docs`

_Lembre-se de adicionar a sua API_KEY (definida no arquivo .env) no campo de autorização da documentação para poder testar os endpoints protegidos._

## Observação
Este projeto foi desenvolvido para fins de estudo e como portfólio técnico. Embora siga boas práticas de desenvolvimento, ele pode conter bugs ou falhas. A intenção principal é demonstrar o conhecimento e a aplicação das tecnologias mencionadas em uma arquitetura de microsserviços.
