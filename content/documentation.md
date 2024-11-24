<h3>Documentation</h3><br>

Sure! Here's a detailed technical report for the entire script. I’ll break it down by each section and function, explaining what they do:

---

## **Technical Report: Anomaly Detection and Security Enforcement Script**

### **1. Imports and Setup**
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
```
- **Libraries**:
  - `pandas` & `numpy`: Used for data manipulation and numerical operations.
  - `sklearn`: Provides machine learning models (Isolation Forest, One-Class SVM) and preprocessing tools.
  - `keras`: Used to build and train the autoencoder neural network.
  - `geopy` & `geoip2`: For geolocation services to detect IP spoofing.
  - `matplotlib`: For generating and saving plots (e.g., visualizations of risk scores).
  - `os`: For handling file operations (e.g., saving files to a directory).
  - `smtplib`, `MIMEText`, `MIMEMultipart`: For sending email alerts when suspicious activity is detected.

---

### **2. Output Directory Setup**
```python
output_dir = './output_files'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
```
- **Purpose**: Creates a directory (`output_files`) where all output files (e.g., risk scores, blocked IPs, images) will be stored.

---

### **3. Data Preprocessing**
```python
def preprocess_data(data):
    scaler = StandardScaler()
    data['ClientSrcPort'] = scaler.fit_transform(data['ClientSrcPort'].values.reshape(-1, 1))
    data['ClientDstPort'] = scaler.fit_transform(data['ClientDstPort'].values.reshape(-1, 1))
    return data
```
- **Purpose**: 
  - Standardizes the `ClientSrcPort` and `ClientDstPort` features to have zero mean and unit variance, which improves the performance of machine learning models.
  
---

### **4. Anomaly Detection with Multiple Models**
The script uses multiple methods for anomaly detection, ensuring robust identification of malicious activities.

#### **Isolation Forest**
```python
def isolation_forest_detection(data, contamination=0.05):
    iso_forest = IsolationForest(contamination=contamination, random_state=42)
    iso_pred = iso_forest.fit_predict(data)
    return iso_pred
```
- **Purpose**: 
  - Detects anomalies based on an ensemble of trees. The `contamination` parameter specifies the expected proportion of outliers in the data.
  
#### **One-Class SVM**
```python
def one_class_svm_detection(data):
    svm = OneClassSVM(kernel="rbf", gamma='scale', nu=0.05)
    svm_pred = svm.fit_predict(data)
    return svm_pred
```
- **Purpose**: 
  - Uses the One-Class SVM method to detect anomalies based on a non-linear decision boundary.

#### **Autoencoder (Neural Network)**
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
```
- **Purpose**: 
  - A deep learning model built using Keras. The autoencoder learns to compress the input data (encoding) and then reconstruct it (decoding). Anomalies are detected based on the reconstruction error.

```python
def autoencoder_detection(data, autoencoder, epochs=50, batch_size=32):
    autoencoder.fit(data, data, epochs=epochs, batch_size=batch_size)
    reconstructed = autoencoder.predict(data)
    reconstruction_error = np.mean(np.abs(data - reconstructed), axis=1)
    return reconstruction_error
```
- **Purpose**: 
  - Trains the autoencoder and computes the reconstruction error. Higher errors indicate anomalies.

---

### **5. Unsupervised Learning for Novel Attack Detection (DBSCAN)**
```python
def unsupervised_detection(data):
    dbscan = DBSCAN(eps=0.3, min_samples=10)
    dbscan_labels = dbscan.fit_predict(data)
    
    silhouette_avg = silhouette_score(data, dbscan_labels)
    print(f"Silhouette Score for DBSCAN: {silhouette_avg}")
    
    return dbscan_labels
```
- **Purpose**: 
  - Uses DBSCAN (Density-Based Spatial Clustering) to identify clusters of similar data points. It also computes the silhouette score to evaluate how well the clustering worked.

---

### **6. GeoIP-based IP Spoofing Detection**
```python
def ip_spoofing_detection(ip_list):
    reader = geoip2.database.Reader('/path/to/GeoLite2-City.mmdb')
    spoofing_flags = []
    
    for ip in ip_list:
        response = reader.city(ip)
        if response.location.latitude is None or response.location.longitude is None:
            spoofing_flags.append(True)
        else:
            spoofing_flags.append(False)
    
    return spoofing_flags
```
- **Purpose**: 
  - Detects potential IP spoofing by checking the geographical location of IP addresses. If the location data is invalid or inconsistent, the IP is flagged as suspicious.

---

### **7. Port Scanning Detection**
```python
def port_scanning_detection(data):
    port_scanning_flags = []
    unique_ips = data['ClientIP'].unique()
    
    for ip in unique_ips:
        ip_data = data[data['ClientIP'] == ip]
        if ip_data['ClientSrcPort'].nunique() > 10:
            port_scanning_flags.append(True)
        else:
            port_scanning_flags.append(False)
    
    return port_scanning_flags
```
- **Purpose**: 
  - Detects potential port scanning behavior by identifying IP addresses that use more than a certain number of source ports (indicating scanning activity).

---

### **8. Man-in-the-Middle (MITM) Attack Detection (Placeholder)**
```python
def mitm_detection(data):
    return [False] * len(data)
```
- **Purpose**: 
  - Placeholder function for MITM attack detection. In a real scenario, this could analyze SSL/TLS handshakes or HTTP headers for anomalies.

---

### **9. Policy Enforcement (Alerts and Blocking)**
```python
def enforce_security_policy(risk_scores, threshold=0.8):
    risky_ips = []
    
    for i, score in enumerate(risk_scores):
        if score > threshold:
            risky_ips.append(i)
    
    blocked_ips = block_risky_ips(risky_ips)
    send_alert_email(risky_ips)

    return risky_ips, blocked_ips
```
- **Purpose**: 
  - Enforces a security policy by identifying risky IPs with a risk score above a threshold. It blocks these IPs and sends an alert via email.

#### **Block Risky IPs**
```python
def block_risky_ips(risky_ips):
    blocked_ips = risky_ips
    save_to_file(blocked_ips, 'blocked_ips.txt')
    print(f"Blocked IPs: {blocked_ips}")
    return blocked_ips
```
- **Purpose**: 
  - Simulates blocking risky IPs and saves them to a file (`blocked_ips.txt`). In a real system, this would interact with network/firewall tools.

#### **Send Alert Email**
```python
def send_alert_email(risky_ips):
    sender_email = "your_email@example.com"
    receiver_email = "admin@example.com"
    subject = "Security Alert: Suspicious Activity Detected"
    
    body = f"Alert: The following IP addresses are exhibiting suspicious activity: {risky_ips}"
    
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    
    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login(sender_email, 'your_password')
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Alert sent successfully.")
    except Exception as e:
        print(f"Error sending alert: {e}")
```
- **Purpose**: 
  - Sends an email alert to an admin when risky IPs are detected.

---

### **10. Save Results and Images**
```python
def save_to_file(data, filename):
    if isinstance(data, list):
        with open(os.path.join(output_dir, filename), 'w') as f:
            f.write("\n".join(map(str, data)))
    elif isinstance(data, pd.DataFrame):
        data.to_csv(os.path.join(output_dir, filename), index=False)
```
- **Purpose**: 
  - Saves detection results (e.g., risky IPs or dataframes) to text or CSV files.

```python
def save_image(fig, filename):


    fig.savefig(os.path.join(output_dir, filename))
    print(f"Image saved to {filename}")
```
- **Purpose**: 
  - Saves matplotlib figures (e.g., risk score plots) to image files.

---

### **11. Putting It All Together**
```python
data = pd.read_csv('network_traffic_data.csv')
data = preprocess_data(data)

iso_pred = isolation_forest_detection(data)
svm_pred = one_class_svm_detection(data)
autoencoder = build_autoencoder(data.shape[1])
reconstruction_error = autoencoder_detection(data, autoencoder)

dbscan_labels = unsupervised_detection(data)
spoofing_flags = ip_spoofing_detection(data['ClientIP'].values)
port_scanning_flags = port_scanning_detection(data)
mitm_flags = mitm_detection(data)

risk_scores = np.mean([iso_pred, svm_pred, reconstruction_error > np.percentile(reconstruction_error, 95)], axis=0)
risky_ips, blocked_ips = enforce_security_policy(risk_scores)

print(f"Detected risky IPs: {risky_ips}")

fig, ax = plt.subplots()
ax.plot(risk_scores)
ax.set_title("Risk Scores Plot")
save_image(fig, 'risk_scores_plot.png')

save_to_file(risky_ips, 'risky_ips.txt')
save_to_file(pd.DataFrame({'IP': risky_ips, 'Score': risk_scores}), 'risky_ips.csv')
```
- **Purpose**: 
  - This is the main workflow of the script. It loads and preprocesses data, applies anomaly detection models, detects spoofing and port scanning, computes risk scores, enforces security policies, and saves the results.

---

This concludes the technical breakdown of the script. Each section performs a specific task aimed at detecting security threats, providing alerts, and saving analysis results for future review.
