# Snoopy Finance: Seu Amigo para o Controle Financeiro

![Snoopy Feliz](./gerenciador_app/frontEnd/static/images/image_project.png)  

O **Snoopy Finance** é uma aplicação web de controle financeiro pessoal que transforma a maneira como você gerencia seu dinheiro. Com um foco obsessivo na experiência do usuário, a plataforma oferece uma interface reativa, divertida e intuitiva, inspirada no universo do Snoopy. Através de técnicas como **Optimistic UI**, garantimos que suas interações sejam instantâneas, eliminando a sensação de atraso e tornando o controle de suas finanças uma tarefa leve e agradável.

## ✨ Funcionalidades Chave

- **Dashboard Reativo com Optimistic UI**: O frontend, construído com Alpine.js, atualiza saldos e riscos na tabela instantaneamente ao clicar. A sincronização com o backend ocorre em segundo plano, proporcionando uma experiência de usuário fluida e sem interrupções.

- **Snoopy Interativo**: O mascote reage dinamicamente à sua saúde financeira. Ele fica feliz quando suas finanças estão em ordem, neutro em situações normais e preocupado quando é hora de ter mais atenção, oferecendo um feedback visual imediato e lúdico.

- **CRUD com Modais**: Adicione, edite e remova gastos e entradas de forma rápida e eficiente, sem precisar sair da tela principal do dashboard. Tudo acontece em modais elegantes e diretos.

- **Sistema de Login Completo**: Segurança é fundamental. O Snoopy Finance conta com um sistema de autenticação robusto, utilizando sessões seguras com Flask-Login e hashing de senhas com Flask-Bcrypt, garantindo que seus dados financeiros estejam sempre protegidos e isolados.

- **Relatórios Gráficos Inteligentes**: Visualize seus dados de forma clara com gráficos de rosca duplos, gerados com Chart.js. Analise suas despesas por categoria e por banco, permitindo uma compreensão aprofundada de seus hábitos financeiros.

## 🛠️ Tech Stack & Arquitetura

O projeto foi construído com uma seleção de tecnologias modernas e eficientes, visando performance, escalabilidade e uma ótima experiência de desenvolvimento.

| Categoria   | Tecnologia/Ferramenta                                                                                                                                                           | Propósito                                                                                                  |
| :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :--------------------------------------------------------------------------------------------------------- |
| **Backend** | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white) ![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white) | Microframework leve para a API, servido por um WSGI robusto para produção.                                  |
| **Frontend**| ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white) ![Alpine.js](https://img.shields.io/badge/Alpine.js-8BC0D0?style=for-the-badge&logo=alpine.js&logoColor=black) ![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chart.js&logoColor=white) | Estrutura semântica, estilização utilitária, reatividade leve e visualização de dados interativa.            |
| **Database**| ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white) | Banco de dados relacional robusto (servido pela Neon Tech) e ORM para mapeamento objeto-relacional.        |
| **Auth**    | ![Flask-Login](https://img.shields.io/badge/Flask--Login-000000?style=for-the-badge) ![Flask-Bcrypt](https://img.shields.io/badge/Flask--Bcrypt-000000?style=for-the-badge) | Gerenciamento de sessões de usuário e hashing seguro de senhas.                                            |
| **Dados**   | ![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)                                                                                   | Utilizado para agrupamento e manipulação de dados para a geração dos relatórios gráficos.                  |
| **Deploy**  | ![Railway](https://img.shields.io/badge/Railway-0B0D12?style=for-the-badge&logo=railway&logoColor=white)                                                                                 | Plataforma de infraestrutura como serviço para deploy contínuo e simplificado.                             |

A arquitetura do backend segue o padrão **Layered Architecture**, separando as responsabilidades em três camadas distintas para maior organização e manutenibilidade:

- **Controller Layer**: Responsável por receber as requisições HTTP, validar dados de entrada e orquestrar a resposta.
- **Service Layer**: Contém a lógica de negócio da aplicação, processando os dados e tomando as decisões.
- **Model Layer**: Define a estrutura dos dados e gerencia a interação com o banco de dados através do SQLAlchemy.

## 🚀 Instalação e Execução Local

Para executar o Snoopy Finance em seu ambiente local, siga os passos abaixo.

### Pré-requisitos

- Python 3.x
- PostgreSQL

### Passo a Passo

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/seu-usuario/snoopy-finance.git
    cd snoopy-finance
    ```

2.  **Crie e ative um ambiente virtual:**

    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**

    Crie um arquivo `.env` na raiz do projeto, copiando o `.env.example`. Preencha as variáveis necessárias:

    ```env
    # Exemplo de .env
    DATABASE_URL="postgresql://usuario:senha@host:porta/database"
    SECRET_KEY="uma-chave-secreta-muito-forte"
    ```

5.  **Execute o script de setup do banco de dados:**

    Este comando criará as tabelas necessárias no seu banco de dados PostgreSQL.

    ```bash
    python create_tables.py
    ```

6.  **Inicie a aplicação:**

    ```bash
    python run.py
    ```

    A aplicação estará disponível em `http://127.0.0.1:5000`.

---

Feito com ❤️ por [Nelson](https://github.com/Nelsolaa).
