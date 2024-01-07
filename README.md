# Projeto Final BD2

## Como executar o projeto com docker
O docker-compose vai criar dois containers:
- Um container para a base de dados postgres
- Um container para a aplicação django
- Um container para o mongoDB

Ao criar o container da aplicação django é executado um [script em python](initialize_db.py) que gera a base de dados, objetos, utilizadores e dados de teste.
São também criados utilizadores do django para acesso à aplicação ([ver seção utilizadores](#utilizadores-django-criados) ).

```bash
.\start.bat
```
ou
```bash
docker compose -f docker-compose.yml up -d
```

## Como executar o projeto sem docker
Esta é uma tarefa mais complexa, pois é necessário instalar o python, django e as dependências do projeto.
Para executar o projeto sem docker é necessário:
- Instalar o python 3.9
- Instalar as dependências do projeto (ver [requirements.txt](requirements.txt))
- Criar a base de dados postgres
- Executar o script [initialize_db.py](initialize_db.py) para gerar a base de dados, objetos, utilizadores e dados de teste.
- Executar o servidor django

```bash
python manage.py runserver
```


## Utilizadores django criados

| Username      |   Password    |
|---------------|:-------------:|
| admin         | admin         |
| compras       | compras       |
| vendas        | vendas        |
| producao      | producao      |
| stock         | stock         |

