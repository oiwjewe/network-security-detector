<h3>Documentation</h3><br><br>

Let's break down the code step by step, as if you're walking through it during a single session. This will help you understand how each part contributes to the overall goal of network traffic analysis and security enforcement.

### **Session Walkthrough: Anomaly Detection and Security System**

---

### **1. Importing Required Libraries**

We start by importing the necessary libraries. Each one of these serves a specific purpose:

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

- **Pandas** for data manipulation.
- **Numpy** for numerical operations.
- **Scikit-learn** for machine learning models and preprocessing (e.g., **Isolation Forest**, **One-Class SVM**, **DBSCAN**).
- **Geopy** and **GeoIP2** for IP geolocation and spoofing detection.
- **Matplotlib** for data visualization.
- **Flask** for creating a small web server to serve output.
- **Smtplib** and email MIME libraries for sending email alerts.

---

### **2. Setting Up Output Directory**

Before processing any data, we ensure there is a folder to store output files:

```python
output_dir = './output_files'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
```

- This section checks if the `output_files` directory exists. If not, it creates one. This ensures that any analysis results, like files or images, will be saved in an organized way.

---

### **3. Data Preprocessing**

Next, we preprocess the data to ensure that all features are on the same scale for accurate analysis:

```python
def preprocess_data(data):
    scaler = StandardScaler()
    data['ClientSrcPort'] = scaler.fit_transform(data['ClientSrcPort'].values.reshape(-1, 1))
    data['ClientDstPort'] = scaler.fit_transform(data['ClientDstPort'].values.reshape(-1, 1))
    return data
```

- **StandardScaler** is used to normalize `ClientSrcPort` (source port) and `ClientDstPort` (destination port) so that they have a mean of 0 and a standard deviation of 1. This helps ensure that machine learning models perform optimally without bias towards higher values of any feature.

---

### **4. Anomaly Detection**

This part applies multiple models for anomaly detection to identify abnormal network traffic.

#### **4.1 Isolation Forest for Anomaly Detection**

```python
def isolation_forest_detection(data, contamination=0.05):
    iso_forest = IsolationForest(contamination=contamination, random_state=42)
    iso_pred = iso_forest.fit_predict(data)
    return iso_pred
```

- **Isolation Forest** detects anomalies by isolating them in the data. The `contamination` parameter specifies how much of the data is expected to be anomalous (5% here).
- It returns `-1` for anomalies and `1` for normal data.

#### **4.2 One-Class SVM for Anomaly Detection**

```python
def one_class_svm_detection(data):
    svm = OneClassSVM(kernel="rbf", gamma='scale', nu=0.05)
    svm_pred = svm.fit_predict(data)
    return svm_pred
```

- **One-Class SVM** is another anomaly detection technique. It tries to learn a boundary around normal data and flags any data points outside that boundary as anomalies.

---

### **5. Unsupervised Learning for Novel Attack Detection**

In this section, we use DBSCAN, an unsupervised clustering algorithm, to find novel attack patterns.

```python
def unsupervised_detection(data):
    dbscan = DBSCAN(eps=0.3, min_samples=10)
    dbscan_labels = dbscan.fit_predict(data)
    
    silhouette_avg = silhouette_score(data, dbscan_labels)
    print(f"Silhouette Score for DBSCAN: {silhouette_avg}")
    
    return dbscan_labels
```

- **DBSCAN** identifies clusters of data points that are closely packed together. Points in low-density regions are labeled as outliers (novel attacks).
- **Silhouette Score** evaluates the quality of clustering, with higher values indicating better-defined clusters.

---

### **6. GeoIP-Based IP Spoofing Detection**

This function detects potential IP spoofing by checking the geolocation of IP addresses.

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

- **GeoIP** is used to verify the geographic location of an IP address. If the latitude and longitude are not found, it suggests that the IP might be spoofed (i.e., it is hiding its true location).

---

### **7. Port Scanning Detection**

We detect suspicious port scanning behavior by analyzing the number of unique ports accessed by each IP.

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

- Port scanning is typically detected when an IP accesses a large number of ports. Here, we flag any IP accessing more than 10 ports as a potential port scanner.

---

### **8. Placeholder for MITM Detection**

Currently, MITM (Man-in-the-Middle) attack detection is a placeholder and doesn't perform actual analysis:

```python
def mitm_detection(data):
    return [False] * len(data)  # Return dummy values (no detection for now)
```

- MITM detection would require further analysis, such as inspecting packet integrity or session anomalies. For now, it returns a list of `False` values, implying no detection.

---

### **9. Policy Enforcement (Alerts and Blocking)**

This section blocks risky IPs and sends alerts to administrators.

#### **9.1 Blocking Risky IPs**

```python
def block_risky_ips(risky_ips):
    blocked_ips = risky_ips
    save_to_file(blocked_ips, 'blocked_ips.txt')  # Save the blocked IPs to a text file
    print(f"Blocked IPs: {blocked_ips}")
    return blocked_ips
```

- **Block risky IPs**: Here, risky IPs are "blocked" by simply saving them to a text file. In a real system, you would integrate with a firewall or security tool to block these IPs.

#### **9.2 Sending Alert Emails**

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

- **Alert system**: If risky IPs are detected, an email is sent to the system administrator with the details. You would replace the email settings with your own configurations.

---

### **10. Saving Results and Visualizations**

We save results to files and create visualizations of the risk scores.

```python
def save_to_file(data, filename):
    if isinstance(data, list):  # Save as text file if it's a list
        with open(os.path.join(output_dir, filename), 'w') as f:
            f.write("\n".join(map(str, data)))
    elif isinstance(data, pd.DataFrame):  # Save as CSV if it's a DataFrame
        data.to_csv(os.path.join(output_dir, filename), index=False)

def save_image(fig, filename):
    fig.savefig(os.path.join(output_dir, filename))
    print(f"Image saved to {filename}")
```

- **Save output**: Results such as risky IPs and visualizations are saved to files for review.

---

### **11. Putting It All Together**

Finally, we combine all parts of the system to run the analysis and enforce security policies:

```python
# Load and preprocess data (replace with your actual data)
data = pd.read_csv('network_traffic_data.csv')

# Preprocessing
data = preprocess_data(data)

# Apply multiple anomaly detection models
iso_pred = isolation_forest_detection(data)
svm_pred = one_class_svm_detection(data)

# Unsupervised learning for novel attacks (using DBSCAN)
dbscan_labels = unsupervised_detection(data)

# Detect spoofed

 IPs using GeoIP
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
```

- **Main analysis loop**: All the preprocessing, anomaly detection, spoofing detection, and policy enforcement steps are executed in sequence. The results are saved, and visualizations are created for the administrator to review.

---

### **12. Web Interface with Flask**

Lastly, we use Flask to serve the results:

```python
app = Flask(__name__)

@app.route('/view/<filename>')
def view_file(filename):
    return send_from_directory(output_dir, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=('cert.pem', 'key.pem'))  # Run with SSL
```

- **Flask app**: A web server is set up to allow an administrator to view the saved files and visualizations via their browser.

---

This concludes our session. Every function and part of the code contributes to analyzing network traffic, detecting anomalies, and enforcing security measures.
