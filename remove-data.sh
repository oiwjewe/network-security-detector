#!/bin/bash

# Caminho do arquivo no container (pode ser um diretório ou arquivo específico)
CAMINHO_ARQUIVO="/caminho/no/container/*.csv" #alterar

# Nome do container
CONTAINER="meu_container" #alterar

# Remover o arquivo (ou arquivos) .csv do container
docker exec $CONTAINER rm $CAMINHO_ARQUIVO

# (Opcional) Verificar se o arquivo foi removido (você pode adicionar outros comandos de verificação)
docker exec $CONTAINER ls $CAMINHO_ARQUIVO
