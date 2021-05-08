# MTG Stats


## Instalando o repositório

Na pasta raíz, executar:

```
pip install . -r requirements.txt
```

## Rodando os testes

Na pasta raíz do repositório, executar

```
./src/tests/run_tests.py
```

Esse script executa as buscas em src/tests/data/test_queries.txt e gera os arquivos de cartas correspondentes
na pasta /data, cada linha do aquivo é

```
<nome_do_arquivo>|<query do scryfall>
```

Você pode usar o parametro ```--no-cache``` para forçar o Download de arquivos que já existem