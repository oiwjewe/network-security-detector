# Technical Documentation for `geoip.sh` Script

This `geoip.sh` script automates the process of downloading the GeoLite2 City database, installing necessary Python dependencies, and training an anomaly detection model using the Isolation Forest algorithm. Below is a breakdown of each section of the script:

---

### 1. **Download the GeoLite2 City Database**

```bash
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
```

- **Purpose**: Downloads and extracts the GeoLite2 City database, which provides location-based information (such as city, country, and other details) based on IP addresses.
- **Explanation**:
  - `GEOIP_URL`: Defines the URL for the GeoLite2 City database in a compressed `.tar.gz` format.
  - `GEOIP_TAR`: Specifies the name of the temporary `.tar.gz` file to store the downloaded content.
  - `GEOIP_DB`: Represents the final `.mmdb` database file name.
  - `wget $GEOIP_URL -O $GEOIP_TAR`: Downloads the database archive from the specified URL and saves it as `GeoLite2-City.tar.gz`.
  - `tar -xvzf $GEOIP_TAR`: Extracts the contents of the `.tar.gz` file. The `-xvzf` flags indicate extraction, verbose output, and file compression handling.
  - `rm $GEOIP_TAR`: Deletes the `.tar.gz` file after extraction to clean up and save space.

---

### 2. **Install Python Dependencies**

```bash
echo "Instalando dependências Python..."
pip install --upgrade pip
pip install -r requirements.txt
```

- **Purpose**: Installs the required Python dependencies specified in a `requirements.txt` file. This is necessary for the script and model training to run properly.
- **Explanation**:
  - `pip install --upgrade pip`: Upgrades the `pip` tool to the latest version to ensure that all Python packages can be installed smoothly.
  - `pip install -r requirements.txt`: Installs all Python packages listed in the `requirements.txt` file. These dependencies are necessary for the Python environment to run the application, including libraries such as `sklearn`, `numpy`, and others.

---

### 3. **Train Anomaly Detection Model**

```bash
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
```

- **Purpose**: Trains an anomaly detection model using random data and the Isolation Forest algorithm. The trained model is then saved as a `.pkl` file for later use.
- **Explanation**:
  - `python3 -c` allows running a Python script directly from the command line, embedded within the Bash script.
  - The script uses `numpy` to generate random data and `sklearn.ensemble.IsolationForest` to train an anomaly detection model:
    - `X_train = np.random.rand(100, 2)`: Generates 100 random samples, each with 2 features (representing a simple 2D dataset).
    - `model = IsolationForest()`: Creates an Isolation Forest model, which is used for detecting anomalies in the data.
    - `model.fit(X_train)`: Trains the model using the generated random data (`X_train`).
    - The model is saved to a file named `anomaly_model.pkl` using Python's `pickle` module, which serializes the model object for later use.

---

This script sets up the environment by downloading the required database, installing dependencies, and preparing a trained model for anomaly detection, with each step clearly separated for easy execution and maintenance.
