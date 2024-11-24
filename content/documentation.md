<h3>Documentation</h3><br><br>

Here is a detailed, section-by-section explanation of the script, outlining what each part does:

---

### **Imports**
```python
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
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
from flask import Flask, send_from_directory
```
**Explanation**:
- **pandas**: Used for data manipulation, particularly for reading CSV files and handling data frames.
- **numpy**: Used for numerical operations, such as calculating mean values for risk scores.
- **sklearn.ensemble.IsolationForest, sklearn.svm.OneClassSVM**: Used for anomaly detection through Isolation Forest and One-Class SVM models.
- **sklearn.preprocessing.StandardScaler**: Used to normalize the data features.
- **geopy.distance**: A library for calculating geographical distances (although not used in the code directly).
- **geoip2.database**: Used for geolocation-based IP spoofing detection by checking IP addresses against a GeoIP database.
- **sklearn.cluster.DBSCAN**: Used for unsupervised clustering of data points to detect novel attacks.
- **sklearn.metrics.silhouette_score**: Used to evaluate the clustering results from DBSCAN.
- **smtplib**: Provides email functionality for sending alerts.
- **email.mime.text, email.mime.multipart**: Used to structure and send email alerts.
- **matplotlib.pyplot**: Used for generating visualizations (like histograms of risk scores).
- **os**: Used for file handling and directory creation.
- **Flask**: A micro web framework for serving files (e.g., visualizations).

---

### **Output Directory Setup**
```python
output_dir = './output_files'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
```
**Explanation**:
- This part creates a directory called `./output_files` if it does not already exist. This directory will be used to save output files such as blocked IPs and visualizations.

---

### **Step 1: Data Preprocessing**
```python
def preprocess_data(data):
    # Normalize traffic volume and other necessary features
    scaler = StandardScaler()
    data['ClientSrcPort'] = scaler.fit_transform(data['ClientSrcPort'].values.reshape(-1, 1))
    data['ClientDstPort'] = scaler.fit_transform(data['ClientDstPort'].values.reshape(-1, 1))
    return data
```
**Explanation**:
- This function normalizes the `ClientSrcPort` and `ClientDstPort` columns in the data. 
- It uses `StandardScaler` from scikit-learn to scale the values to have a mean of 0 and a standard deviation of 1, which is a common preprocessing step before applying machine learning models.

---

### **Step 2: Anomaly Detection with Multiple Models**

**Isolation Forest**
```python
def isolation_forest_detection(data, contamination=0.05):
    iso_forest = IsolationForest(contamination=contamination, random_state=42)
    iso_pred = iso_forest.fit_predict(data)
    return iso_pred
```
**Explanation**:
- This function applies the `IsolationForest` algorithm to detect anomalies in the data. 
- The `contamination` parameter defines the proportion of outliers in the data (set to 5% here). 
- The `fit_predict()` function fits the model and predicts whether each data point is an outlier (-1) or normal (1).

**One-Class SVM**
```python
def one_class_svm_detection(data):
    svm = OneClassSVM(kernel="rbf", gamma='scale', nu=0.05)
    svm_pred = svm.fit_predict(data)
    return svm_pred
```
**Explanation**:
- This function uses a `OneClassSVM` to detect outliers (anomalies). 
- The `kernel="rbf"` specifies the use of the radial basis function kernel, and `gamma='scale'` sets the kernel coefficient.
- The `nu=0.05` parameter specifies the proportion of outliers (set to 5%).
- The `fit_predict()` method trains the model on the data and predicts outliers (returning -1 for anomalies and 1 for normal data).

---

### **Step 3: Unsupervised Learning for Novel Attack Detection**

```python
def unsupervised_detection(data):
    dbscan = DBSCAN(eps=0.3, min_samples=10)
    dbscan_labels = dbscan.fit_predict(data)
    
    # Silhouette Score for evaluating clustering
    silhouette_avg = silhouette_score(data, dbscan_labels)
    print(f"Silhouette Score for DBSCAN: {silhouette_avg}")
    
    return dbscan_labels
```
**Explanation**:
- This function applies `DBSCAN` (Density-Based Spatial Clustering of Applications with Noise) for unsupervised learning to detect clusters in the data. 
- The `eps=0.3` parameter defines the maximum distance between two samples for them to be considered as part of the same neighborhood, and `min_samples=10` sets the minimum number of samples required to form a cluster.
- The `silhouette_score` evaluates how well the clustering algorithm performed, providing a value between -1 and 1 (higher values indicate better-defined clusters).
- The function returns the cluster labels for each data point.

---

### **Step 4: GeoIP-based IP Spoofing Detection**
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
**Explanation**:
- This function uses the `geoip2` library to check the geolocation of each IP address in the provided `ip_list`.
- If the geolocation data (latitude or longitude) is missing, the IP is flagged as possibly spoofed.
- The function returns a list of boolean flags (`True` for spoofed, `False` for valid).

---

### **Step 5: Port Scanning Detection**
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
**Explanation**:
- This function detects potential port scanning activities by checking how many unique ports each IP address accesses.
- If an IP accesses more than 10 unique ports, it is flagged as a port scanner.
- The function returns a list of boolean flags indicating whether each IP address is performing a port scan.

---

### **Step 6: MITM Attack Detection (Placeholder)**
```python
def mitm_detection(data):
    # Placeholder for MITM detection
    return [False] * len(data)  # Return dummy values (no detection for now)
```
**Explanation**:
- This is a placeholder function for detecting Man-in-the-Middle (MITM) attacks. Currently, it simply returns a list of `False` values, indicating no detection.

---

### **Step 7: Policy Enforcement (Alerts and Blocking)**

**Enforce Security Policy**
```python
def enforce_security_policy(risk_scores, threshold=0.8):
    risky_ips = []
    
    for i, score in enumerate(risk_scores):
        if score > threshold:
            risky_ips.append(i)  # Collect risky IP indices
    
    # Simulate blocking risky IPs
    blocked_ips = block_risky_ips(risky_ips)
    
    # Simulate sending alert via email
    send_alert_email(risky_ips)

    return risky_ips, blocked_ips
```
**Explanation**:
- This function checks if the risk scores exceed a threshold (default 0.8). 
- IPs that are above the threshold are considered risky.
- The function calls `block_risky_ips` to simulate blocking the risky IPs and `send_alert_email` to simulate sending an email alert.

**Blocking Risky IPs**
```python
def block_risky_ips(risky_ips):
    # Simulate blocking risky IPs by logging them into a blocked list.
    blocked_ips = risky_ips  # Just simulate by returning the same IPs for now
    save_to_file(blocked_ips, 'blocked_ips.txt')  # Save blocked IPs to a text file
    print(f"Blocked IPs: {blocked_ips}")
    return blocked_ips
```
**Explanation**:
- This function simulates blocking risky IPs by saving them to a file (`blocked_ips.txt`) and printing them.

**Sending Alert Email**
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
**Explanation**:
- This function sends an email alert about risky IPs.
- It uses `smtplib` to send the email through an SMTP server.

---

### **Step 8: Putting It All Together**

This section orchestrates all of the functions to process the data, detect anomalies, assess risks, and take actions:
```python
data = pd.read_csv('network_traffic_data.csv')

# Preprocessing
data = preprocess_data(data)

# Apply multiple anomaly detection models
iso_pred = isolation_forest_detection(data)
svm_pred = one_class_svm_detection(data)

# Unsupervised learning for novel attacks (using DBSCAN)
dbscan_labels = unsupervised_detection(data)

# Detect spoofed IPs using GeoIP
spoofing_flags = ip_spoofing_detection(data['ClientIP'].values)

# Detect port scanning behavior
port_scanning_flags = port_scanning_detection(data)

# MITM detection (currently a placeholder)
mitm_flags = mitm_detection(data)

# Aggregate results and create risk scores
risk_scores = np.mean([iso_pred, svm_pred], axis=0)  # No autoencoder

# Apply policy enforcement: Block or alert on high-risk IPs
risky_ips, blocked_ips = enforce_security_policy(risk_scores)

# Show the results and save output
save_to_file(risky_ips, 'risky_ips.txt')

# Visualizations
plt.figure(figsize=(10, 6))
plt.hist(risk_scores, bins=50, color='blue', alpha=0.7)
plt.title('Risk Scores Distribution')
plt.xlabel('Risk Score')
plt.ylabel('Frequency')
save_image(plt, 'risk_score_histogram.png')

# Serve files via Apache (Flask app for visualization)
app = Flask(__name__)

@app.route('/view/<filename>')
def view_file(filename):
    return send_from_directory(output_dir, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=('cert.pem', 'key.pem'))  # Run with SSL (Apache port 443)
```
**Explanation**:
- The data is loaded and preprocessed.
- Anomaly detection models (`IsolationForest` and `One-Class SVM`) are applied.
- Unsupervised learning is performed using DBSCAN to detect novel attacks.
- GeoIP-based spoofing detection and port scanning detection are executed.
- MITM detection is currently a placeholder.
- Risk scores are calculated as the mean of the anomaly detection models' results.
- High-risk IPs are identified and flagged for blocking or alerting.
- Results are saved to files and visualized in a histogram.
- The Flask application serves the visualizations via an HTTPS web interface.

--- 

This breakdown explains each section of the script in detail, showing how the components interact and what each part of the code does.
