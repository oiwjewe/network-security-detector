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

# Directory for saving files
output_dir = './output_files'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Step 1: Data Preprocessing
def preprocess_data(data):
    # Normalize traffic volume and other necessary features
    scaler = StandardScaler()
    data['ClientSrcPort'] = scaler.fit_transform(data['ClientSrcPort'].values.reshape(-1, 1))
    data['ClientDstPort'] = scaler.fit_transform(data['ClientDstPort'].values.reshape(-1, 1))
    return data

# Step 2: Anomaly Detection with Multiple Models

# Isolation Forest for Anomaly Detection
def isolation_forest_detection(data, contamination=0.05):
    iso_forest = IsolationForest(contamination=contamination, random_state=42)
    iso_pred = iso_forest.fit_predict(data)
    return iso_pred

# One-Class SVM for Anomaly Detection
def one_class_svm_detection(data):
    svm = OneClassSVM(kernel="rbf", gamma='scale', nu=0.05)
    svm_pred = svm.fit_predict(data)
    return svm_pred

# Autoencoder for Anomaly Detection
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

# Step 3: Implement Unsupervised Learning for Novel Attack Detection

# Using DBSCAN (Density-Based Spatial Clustering of Applications with Noise) to detect novel attack patterns
def unsupervised_detection(data):
    dbscan = DBSCAN(eps=0.3, min_samples=10)
    dbscan_labels = dbscan.fit_predict(data)
    
    # Silhouette Score for evaluating clustering
    silhouette_avg = silhouette_score(data, dbscan_labels)
    print(f"Silhouette Score for DBSCAN: {silhouette_avg}")
    
    return dbscan_labels

# Step 4: GeoIP-based IP Spoofing Detection
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

# Step 5: Port Scanning Detection
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

# Step 6: Man-in-the-Middle (MITM) Attack Detection (Placeholder)
def mitm_detection(data):
    # Placeholder for MITM detection
    # Check for anomalies in SSL/TLS handshakes, or abnormal HTTP headers
    return [False] * len(data)  # Return dummy values (no detection for now)

# Step 7: Policy Enforcement (Alerts and Blocking)
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

def block_risky_ips(risky_ips):
    """
    Simulate blocking risky IPs by logging them into a blocked list.
    In real-world scenarios, you would integrate with your firewall or network security tool.
    """
    blocked_ips = risky_ips  # Just simulate by returning the same IPs for now
    save_to_file(blocked_ips, 'blocked_ips.txt')  # Save the blocked IPs to a text file
    print(f"Blocked IPs: {blocked_ips}")
    return blocked_ips

def send_alert_email(risky_ips):
    """
    Send an email alert when risky IPs are detected.
    """
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

def save_to_file(data, filename):
    """
    Save analysis results to file (CSV for lists, TXT for simple data).
    """
    if isinstance(data, list):  # Save as text file if it's a list of IPs or simple data
        with open(os.path.join(output_dir, filename), 'w') as f:
            f.write("\n".join(map(str, data)))
    elif isinstance(data, pd.DataFrame):  # Save as CSV if it's a DataFrame
        data.to_csv(os.path.join(output_dir, filename), index=False)

def save_image(fig, filename):
    """
    Save a matplotlib figure to an image file.
    """
    fig.savefig(os.path.join(output_dir, filename))
    print(f"Image saved to {filename}")

# Step 8: Putting It All Together

# Load and preprocess data (replace with your actual data)
data = pd.read_csv('network_traffic_data.csv')

# Preprocessing
data = preprocess_data(data)

# Apply multiple anomaly detection models
iso_pred = isolation_forest_detection(data)
svm_pred = one_class_svm_detection(data)
autoencoder = build_autoencoder(data.shape[1])
reconstruction_error = autoencoder_detection(data, autoencoder)

# Unsupervised learning for novel attacks (using DBSCAN)
dbscan_labels = unsupervised_detection(data)

# Detect spoofed IPs using GeoIP
spoofing_flags = ip_spoofing_detection(data['ClientIP'].values)

# Detect port scanning behavior
port_scanning_flags = port_scanning_detection(data)

# MITM detection (currently a placeholder)
mitm_flags = mitm_detection(data)

# Aggregate results and create risk scores
risk_scores = np.mean([iso_pred, svm_pred, reconstruction_error > np.percentile(reconstruction_error, 95)], axis=0)

# Apply policy enforcement: Block or alert on high-risk IPs
risky_ips, blocked_ips = enforce_security_policy(risk_scores)

# Show the final detection results
print(f"Detected risky IPs: {risky_ips}")

# Save images generated during execution
# Example: Let's say you generate a plot of the anomaly detection results
fig, ax = plt.subplots()
ax.plot(risk_scores)
ax.set_title("Risk Scores Plot")
save_image(fig, 'risk_scores_plot.png')

# Save the results into files
save_to_file(risky_ips, 'risky_ips.txt')
save_to_file(pd.DataFrame({'IP': risky_ips, 'Score': risk_scores}), 'risky_ips.csv')
