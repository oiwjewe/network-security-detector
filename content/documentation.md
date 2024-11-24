<h3>Documentation</h3>

---

### **Report on Network Security Anomaly Detection Tool**

This document outlines the structure and functionality of a network security system that detects anomalies, potential attacks, and other suspicious behaviors in network traffic. It utilizes a variety of machine learning models, clustering algorithms, geolocation techniques, and email alerting to enhance the security monitoring process.

---

### **1. Importing Required Libraries**

```python
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from keras.models import Model
from keras.layers import Input, Dense
from sklearn.preprocessing import StandardScaler
import geopy.distance
import geoip2.database
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import matplotlib.pyplot as plt
import os
import shutil
from flask import Flask, send_from_directory
```

**Explanation:**
- The code begins by importing a series of essential Python libraries:
  - **Pandas** (`pd`) and **NumPy** (`np`) for data manipulation.
  - **Scikit-learn** libraries for anomaly detection (`IsolationForest`, `OneClassSVM`) and clustering (`DBSCAN`), along with metrics for evaluating clustering quality (`silhouette_score`).
  - **Keras** for deep learning with Autoencoders.
  - **GeoIP2** for geolocation-based analysis of IP addresses.
  - **Smtplib** and **email.mime** for sending email alerts.
  - **Matplotlib** for visualizations.
  - **Flask** to serve files via a web application.

---

### **2. Directory Setup**

```python
# Directory for saving files and visualizations
output_dir = './output_files'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
```

**Explanation:**
- This section checks if the `output_files` directory exists. If it doesn't, it creates it. This folder will store the generated files, such as results and visualizations.

---

### **3. Data Preprocessing**

```python
def preprocess_data(data):
    # Normalize traffic volume and other necessary features
    scaler = StandardScaler()
    data['ClientSrcPort'] = scaler.fit_transform(data['ClientSrcPort'].values.reshape(-1, 1))
    data['ClientDstPort'] = scaler.fit_transform(data['ClientDstPort'].values.reshape(-1, 1))
    return data
```

**Explanation:**
- The `preprocess_data` function normalizes the features `ClientSrcPort` and `ClientDstPort` using `StandardScaler` from Scikit-learn.
  - Normalization ensures that the features are on a comparable scale, improving the performance of machine learning models.

---

### **4. Anomaly Detection with Multiple Models**

#### **a. Isolation Forest for Anomaly Detection**

```python
def isolation_forest_detection(data, contamination=0.05):
    iso_forest = IsolationForest(contamination=contamination, random_state=42)
    iso_pred = iso_forest.fit_predict(data)
    return iso_pred
```

**Explanation:**
- The function `isolation_forest_detection` uses the `IsolationForest` model to identify anomalies in the data.
  - **Contamination** is the expected proportion of outliers, set to 5% by default.
  - The model fits on the data and predicts which points are outliers (represented by -1 for anomalies and 1 for normal points).

#### **b. One-Class SVM for Anomaly Detection**

```python
def one_class_svm_detection(data):
    svm = OneClassSVM(kernel="rbf", gamma='scale', nu=0.05)
    svm_pred = svm.fit_predict(data)
    return svm_pred
```

**Explanation:**
- The function `one_class_svm_detection` applies a One-Class Support Vector Machine (SVM) for anomaly detection.
  - The SVM is trained on normal data and detects outliers by classifying points that do not conform to the learned patterns as anomalies.

#### **c. Autoencoder for Anomaly Detection**

```python
def build_autoencoder(input_dim):
    input_layer = Input(shape=(input_dim,))
    encoded = Dense(64, activation='relu')(input_layer)
    encoded = Dense(32, activation='relu')(encoded)
    encoded = Dense(16, activation='relu')(encoded)
    
    decoded = Dense(32, activation='relu')(encoded)
    decoded = Dense(64, activation='relu')(decoded)
    decoded = Dense(input_dim, activation='sigmoid')(decoded)
    
    autoencoder = Model(input_layer, decoded)
    autoencoder.compile(optimizer='adam', loss='mean_squared_error')
    return autoencoder

def autoencoder_detection(data, autoencoder, epochs=50, batch_size=32):
    autoencoder.fit(data, data, epochs=epochs, batch_size=batch_size)
    reconstructed = autoencoder.predict(data)
    reconstruction_error = np.mean(np.abs(data - reconstructed), axis=1)
    return reconstruction_error
```

**Explanation:**
- **`build_autoencoder`**: This function creates a simple Autoencoder using Keras. The autoencoder learns to compress (encode) and reconstruct (decode) the input data. It’s a deep learning model used to identify anomalies based on reconstruction errors.
- **`autoencoder_detection`**: This function trains the autoencoder and computes the reconstruction error. Points with high reconstruction errors are flagged as anomalies.

---

### **5. Unsupervised Learning for Novel Attack Detection**

```python
def unsupervised_detection(data):
    dbscan = DBSCAN(eps=0.3, min_samples=10)
    dbscan_labels = dbscan.fit_predict(data)
    
    # Silhouette Score for evaluating clustering
    silhouette_avg = silhouette_score(data, dbscan_labels)
    print(f"Silhouette Score for DBSCAN: {silhouette_avg}")
    
    return dbscan_labels
```

**Explanation:**
- The function `unsupervised_detection` applies the **DBSCAN** (Density-Based Spatial Clustering of Applications with Noise) algorithm, which groups data based on density. Outliers (noise) are flagged as -1.
- **Silhouette Score** is calculated to evaluate the quality of the clustering.

---

### **6. GeoIP-based IP Spoofing Detection**

```python
def ip_spoofing_detection(ip_list):
    reader = geoip2.database.Reader('/path/to/GeoLite2-City.mmdb')  # Path to GeoIP database
    spoofing_flags = []
    
    for ip in ip_list:
        response = reader.city(ip)
        if response.location.latitude is None or response.location.longitude is None:
            spoofing_flags.append(True)  # IP geolocation invalid or inconsistent
        else:
            spoofing_flags.append(False)
    
    return spoofing_flags
```

**Explanation:**
- The `ip_spoofing_detection` function uses the **GeoIP2** database to perform geolocation lookups. It checks whether the latitude and longitude of an IP address are available, and flags IPs with invalid or inconsistent location data as potentially spoofed.

---

### **7. Port Scanning Detection**

```python
def port_scanning_detection(data):
    port_scanning_flags = []
    unique_ips = data['ClientIP'].unique()
    
    for ip in unique_ips:
        ip_data = data[data['ClientIP'] == ip]
        if ip_data['ClientSrcPort'].nunique() > 10:  # Example: More than 10 unique ports accessed
            port_scanning_flags.append(True)
        else:
            port_scanning_flags.append(False)
    
    return port_scanning_flags
```

**Explanation:**
- The `port_scanning_detection` function identifies port scanning behavior by checking if an IP address has accessed more than 10 unique ports. This is a simple heuristic for detecting port scanning attacks.

---

### **8. Man-in-the-Middle (MITM) Attack Detection (Placeholder)**

```python
def mitm_detection(data):
    # Placeholder for MITM detection
    # Check for anomalies in SSL/TLS handshakes, or abnormal HTTP headers
    return [False] * len(data)  # Return dummy values (no detection for now)
```

**Explanation:**
- The function `mitm_detection` is a placeholder for detecting man-in-the-middle attacks. Currently, it returns a list of `False` values, implying that no MITM attacks are detected.

---

### **9. Policy Enforcement (Alerts and Blocking)**

```python
def enforce_security_policy(risk_scores, threshold=0.8):
    """
    This function will alert and block IPs based on risk scores above a certain threshold.
    """
    risky_ips = []
    
    for i, score in enumerate(risk_scores):
        if score > threshold:
            risky_ips.append(i)  # Collect risky IP indices
    
    # Simulate blocking risky IPs
    blocked_ips = block_risky_ips(risky_ips)
    
    # Simulate sending alert via email (this can be replaced with your alerting mechanism)
    send_alert_email(risky_ips)

    return risky_ips, blocked_ips
```

**Explanation:**
- The function `enforce_security_policy` checks if any IP has a risk score above a given threshold (0.8 by default). It flags such IPs as risky and calls other functions to simulate blocking these IPs and sending email alerts.

---

### **10. File Saving and Visualization**

```python
def save_to_file(data, filename):
    """
    Save analysis results

 to a file.
    """
    data.to_csv(f"{output_dir}/{filename}.csv", index=False)

def save_image(data, filename):
    """
    Save image file of the data visualization.
    """
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=50)
    plt.title(f"Risk Score Distribution")
    plt.xlabel('Risk Score')
    plt.ylabel('Frequency')
    plt.savefig(f"{output_dir}/{filename}.png")
```

**Explanation:**
- `save_to_file` saves the data (e.g., flagged risky IPs) to a CSV file.
- `save_image` creates a histogram of the risk scores and saves it as an image.

---

### **11. Web Application for Visualization**

```python
app = Flask(__name__)

@app.route('/files/<filename>')
def download_file(filename):
    return send_from_directory(output_dir, filename)

if __name__ == "__main__":
    app.run(ssl_context='adhoc')  # Running with SSL for secure communication
```

**Explanation:**
- A **Flask** web application is set up to serve files, such as analysis results and visualizations, over HTTP. SSL is enabled for secure communication.

---

### **Conclusion**

This system uses machine learning models, geolocation techniques, clustering algorithms, and policy enforcement mechanisms to monitor and detect network anomalies, attacks, and other security threats. The modular approach allows easy extension for new attack detection models, providing a scalable solution for real-time network security monitoring.

---

# Documentation to secundary scripts can be find at:

-[Dockerfile](dockerfile-doc.md) 
-[GeoIP](geo-ip-doc.md)


