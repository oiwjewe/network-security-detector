#!/bin/bash

# 1. Baixar o arquivo GeoLite2-City.mmdb usando wget
echo "Baixando o arquivo GeoLite2-City.mmdb..."
GEOIP_URL="https://geolite.maxmind.com/download/geoip/database/GeoLite2-City.tar.gz"
GEOIP_TAR="GeoLite2-City.tar.gz"
GEOIP_DB="GeoLite2-City.mmdb"

# Baixar o arquivo .tar.gz
wget $GEOIP_URL -O $GEOIP_TAR

# Descompactar o arquivo .tar.gz
tar -xvzf $GEOIP_TAR

# Remover o arquivo .tar.gz após extração
rm $GEOIP_TAR

echo "Arquivo GeoLite2-City.mmdb baixado e extraído com sucesso!"

# 2. Instalar dependências Python
echo "Instalando dependências Python..."
pip install --upgrade pip
pip install -r requirements.txt

# 3. Baixar e treinar o modelo de anomalias
echo "Treinando o modelo de anomalias..."
python3 -c "
import numpy as np
from sklearn.ensemble import IsolationForest
import pickle

# Gerando dados aleatórios
X_train = np.random.rand(100, 2)  # Exemplo de 100 amostras, 2 características

# Treinando o modelo de detecção de anomalias
model = IsolationForest()
model.fit(X_train)

# Salvando o modelo
with open('anomaly_model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

print('Modelo de anomalias treinado e salvo como anomaly_model.pkl.')
"
