<h3>Documentation</h3><br>

Technical Report for Network Traffic Anomaly Detection Script
Overview
This script is designed to analyze network traffic data and detect various types of suspicious activities and security threats. It uses machine learning models to perform anomaly detection, geo-location checks to identify IP spoofing, and implements policy enforcement to take actions on suspicious IPs. The script processes incoming traffic data, applies multiple detection algorithms, and generates output files such as images, CSVs, and text files. These results are also uploaded to an Apache server for centralized storage and access.

1. Data Preprocessing
Function: preprocess_data(data)

The data preprocessing step prepares the network traffic data for analysis by normalizing the features that may vary in scale.

python
Copiar código
def preprocess_data(data):
    # Normalize traffic volume and other necessary features
    scaler = StandardScaler()
    data['ClientSrcPort'] = scaler.fit_transform(data['ClientSrcPort'].values.reshape(-1, 1))
    data['ClientDstPort'] = scaler.fit_transform(data['ClientDstPort'].values.reshape(-1, 1))
    return data
Explanation: This function uses the StandardScaler from sklearn to normalize the ClientSrcPort and ClientDstPort columns, ensuring that the range of values for these features is standardized. This is crucial because different machine learning algorithms may perform poorly if features have vastly different scales. Normalizing ensures that the machine learning models can treat each feature equally.
2. Anomaly Detection Using Multiple Models
The script implements three different machine learning models to detect anomalies in the network traffic data:

a. Isolation Forest
Function: isolation_forest_detection(data, contamination=0.05)

The Isolation Forest model is used to detect anomalies by isolating observations that are different from the rest.

python
Copiar código
def isolation_forest_detection(data, contamination=0.05):
    iso_forest = IsolationForest(contamination=contamination, random_state=42)
    iso_pred = iso_forest.fit_predict(data)
    return iso_pred
Explanation: The Isolation Forest algorithm isolates anomalies by randomly selecting features and splitting the data into partitions. Anomalies are more likely to be isolated early in the process. This function takes the data and fits the Isolation Forest model to detect anomalies, where the contamination parameter specifies the proportion of outliers in the data. The function returns the predicted labels for each data point (1 for normal, -1 for anomalous).
b. One-Class SVM
Function: one_class_svm_detection(data)

The One-Class SVM (Support Vector Machine) model is used for anomaly detection by finding a boundary that separates the normal data from outliers.

python
Copiar código
def one_class_svm_detection(data):
    svm = OneClassSVM(kernel="rbf", gamma='scale', nu=0.05)
    svm_pred = svm.fit_predict(data)
    return svm_pred
Explanation: The One-Class SVM is trained on only the "normal" data (using the fit method) and tries to learn the boundary that separates this data from any potential outliers (anomalies). In the fit_predict() method, it returns 1 for normal data and -1 for anomalies. The model uses an RBF kernel to learn the complex patterns within the data.
c. Autoencoder
Function: build_autoencoder(input_dim) and autoencoder_detection(data, autoencoder, epochs=50, batch_size=32)

Autoencoders are neural networks used for unsupervised anomaly detection. They learn to compress the data into a lower-dimensional representation and reconstruct it. Large reconstruction errors are indicative of anomalies.

python
Copiar código
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
Explanation: The build_autoencoder() function constructs an autoencoder model consisting of an encoder that compresses the input data and a decoder that reconstructs it. During training, the autoencoder learns to minimize the difference between the input and the reconstructed data.
The autoencoder_detection() function fits the model to the data and calculates the reconstruction error for each sample. A high reconstruction error indicates an anomaly, as the model was unable to accurately reconstruct the data point.
3. Unsupervised Learning for Novel Attack Detection
Function: unsupervised_detection(data)

The DBSCAN algorithm is used for detecting novel attack patterns based on clustering.

python
Copiar código
def unsupervised_detection(data):
    dbscan = DBSCAN(eps=0.3, min_samples=10)
    dbscan_labels = dbscan.fit_predict(data)
    
    # Silhouette Score for evaluating clustering
    silhouette_avg = silhouette_score(data, dbscan_labels)
    print(f"Silhouette Score for DBSCAN: {silhouette_avg}")
    
    return dbscan_labels
Explanation: DBSCAN (Density-Based Spatial Clustering of Applications with Noise) is a clustering algorithm that groups together points that are closely packed while marking outliers as noise. The silhouette_score measures how well the data points are clustered. A higher silhouette score indicates better-defined clusters. This method returns the labels for each data point, which could be used to detect novel attacks by identifying noise points.
4. GeoIP-based IP Spoofing Detection
Function: ip_spoofing_detection(ip_list)

This function uses the GeoIP2 library to detect IP spoofing by checking the geolocation data of IP addresses.

python
Copiar código
def ip_spoofing_detection(ip_list):
    reader = geoip2.database.Reader('/path/to/GeoLite2-City.mmdb')
    spoofing_flags = []
    
    for ip in ip_list:
        response = reader.city(ip)
        if response.location.latitude is None or response.location.longitude is None:
            spoofing_flags.append(True)  # IP geolocation invalid or inconsistent
        else:
            spoofing_flags.append(False)
    
    return spoofing_flags
Explanation: The function uses the GeoIP2 database to retrieve geolocation information for each IP address. If the geolocation is invalid or inconsistent, it flags the IP as potentially spoofed. This helps identify malicious activity where attackers might disguise their actual IPs.
5. Policy Enforcement: Block or Alert on High-Risk IPs
Function: enforce_security_policy(risk_scores, threshold=0.8)

This function is responsible for identifying high-risk IPs based on calculated risk scores and taking action (alerting or blocking).

python
Copiar código
def enforce_security_policy(risk_scores, threshold=0.8):
    risky_ips = []
    
    for i, score in enumerate(risk_scores):
        if score > threshold:
            risky_ips.append(i)  # Collect risky IP indices
    
    # Simulate sending alert via email (this can be replaced with your alerting mechanism)
    send_alert_email(risky_ips)

    return risky_ips
Explanation: This function checks if the risk score for an IP exceeds a predefined threshold. If it does, the IP is considered high-risk and is flagged. The function then simulates sending an email alert (via the send_alert_email function). This feature allows for immediate notification of security threats.
6. Saving Results and Uploading Files
The script saves generated output such as plots and CSVs to files, which are then uploaded to an Apache server for centralized access.

Saving Files: The images and analysis results (such as risk scores, anomalous IPs, etc.) are saved locally on the system using standard Python file operations.
Uploading Files: A separate Python script uploads these files to the Apache server for easy access. This helps centralize the analysis results for further investigation or sharing.
Conclusion
This script integrates multiple machine learning models and security techniques to detect anomalies, suspicious activities, and attacks within network traffic data. It combines advanced anomaly detection with machine learning, unsupervised learning, IP geolocation checks, and policy enforcement. Additionally, it automates the process of saving, organizing, and uploading generated reports and images to an Apache server, providing a centralized repository for security professionals to access the results.
