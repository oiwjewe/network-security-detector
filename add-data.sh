#!/bin/bash

# Caminho do arquivo no host
CAMINHO_ARQUIVO="/home/usuario/dados/meuarquivo.csv" #alterar

# Nome do container
CONTAINER="meu_container" #alterar

# Caminho dentro do container
CAMINHO_CONTAINER="/caminho/no/container/meuarquivo.csv" #alterar

# Copiar arquivo do host para o container
docker cp $CAMINHO_ARQUIVO $CONTAINER:$CAMINHO_CONTAINER

# (Opcional) Executar o script dentro do container
docker exec $CONTAINER python /caminho/no/container/seu_script.py
