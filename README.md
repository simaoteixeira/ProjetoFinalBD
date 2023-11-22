
# Projeto Final BD2


## Antes de executar! Dependencias!
Tudo em terminal com permissoes de admin

Instalar pip-tools

 ```bash
pip install pip-tools
```

Instalar dependencias

 ```bash
pip-sync
```

Caso o ficheiro requirements.txt não existir (so houver requirements.in) executar antes 

```bash
pip-compile requirements.in
```
## Utilização

Executar comando no terminal

```bash
ssh aluno4@193.137.7.56 -L 15432:127.0.0.1:5432
```

Só depois executar a aplicação

```bash
ssh aluno4@193.137.7.56 -L 15432:127.0.0.1:5432
```