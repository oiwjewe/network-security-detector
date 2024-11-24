<h3>Documentation</h3><br><br>

Below is a technical documentation for the Dockerfile you've provided. It explains each part of the Dockerfile step-by-step, making it easier to understand and maintain.

---

# Technical Documentation for the Dockerfile

## Overview

This Dockerfile builds a Docker image that serves a Python-based web application using **Apache HTTP Server** with **SSL/TLS** encryption and **Basic Authentication**. It is designed to run a Python web application inside a **non-root user** environment while ensuring security best practices for the Apache server.

The Docker image has two stages:
1. **Build stage**: Where dependencies are installed and the application is prepared.
2. **Runtime stage**: Where the application is served by Apache and configurations like SSL and Basic Authentication are applied.

---

## Stages and Layers Breakdown

### **1. Build Stage**

This stage is responsible for preparing the environment to install dependencies and the application.

#### **Base Image**
```dockerfile
FROM python:3.11-slim as build
```
- **Base Image**: We use the official `python:3.11-slim` image, which is a slim version of Python 3.11, to minimize the image size. 
- **Stage alias**: This stage is named `build`, making it easier to reference in multi-stage builds.

#### **Install Dependencies for Building**
```dockerfile
RUN apt-get update && apt-get install -y build-essential wget tar \
    && apt-get clean
```
- **Install build dependencies**: Installs essential tools needed for building packages or installing dependencies that may require compiling (e.g., `build-essential`, `wget`, `tar`).
- **Clean**: Removes unnecessary files after installation to reduce the image size.

#### **Working Directory**
```dockerfile
WORKDIR /usr/src/network_trf_analyzer
```
- **Set working directory**: Specifies the directory inside the container where the build and subsequent actions (like copying files) will take place.

#### **Copy Application Files**
```dockerfile
COPY . .
```
- **Copy files**: Copies the entire contents of the current directory on the host machine (where the Dockerfile is located) into the `/usr/src/network_trf_analyzer` directory in the container.

---

### **2. Runtime Stage**

This stage prepares the runtime environment by installing the necessary runtime dependencies and configuring the Apache server.

#### **Base Image**
```dockerfile
FROM python:3.11-slim
```
- **Base Image**: Again, we use the `python:3.11-slim` image, as it is lightweight and suitable for runtime environments.

#### **Install Apache and Runtime Dependencies**
```dockerfile
RUN apt-get update && apt-get install -y \
    apache2 \
    apache2-utils \
    ssl-cert \
    python3-pip \
    && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*
```
- **Install Apache**: Installs the `apache2` package, which is the web server that will serve the Python application.
- **Apache Utilities**: Installs `apache2-utils`, which includes tools like `htpasswd` for managing `.htpasswd` files.
- **SSL Certificates**: Installs `ssl-cert` for generating self-signed SSL certificates.
- **Python Pip**: Installs `pip` to manage Python packages inside the container.
- **Clean up**: Removes unnecessary package files to keep the image lean.

#### **Create a Non-Root User**
```dockerfile
RUN useradd -m network_user
```
- **User creation**: Creates a non-root user (`network_user`) to run the application. Running containers as non-root users is a security best practice.

#### **Set the Working Directory and Switch User**
```dockerfile
WORKDIR /usr/src/network_trf_analyzer
USER network_user
```
- **Working directory**: Ensures that the working directory is set to `/usr/src/network_trf_analyzer`, where the application files are located.
- **Switch user**: Switches to the newly created non-root user (`network_user`) for running the application.

#### **Install Python Dependencies**
```dockerfile
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt
```
- **Install Python packages**: Copies the `requirements.txt` (which contains the list of required Python libraries) into the container and installs the dependencies using `pip`.

#### **Disable Unnecessary Apache Modules**
```dockerfile
RUN a2dismod -f status && a2dismod -f autoindex
```
- **Disable unnecessary Apache modules**: The `status` and `autoindex` modules are disabled to reduce the attack surface of the Apache server. 
    - `status`: Disables the server status module.
    - `autoindex`: Disables directory listing (prevents the server from showing a listing of files in a directory if no index file is found).

#### **Enable Required Apache Modules**
```dockerfile
RUN a2enmod ssl headers rewrite
```
- **Enable Apache modules**: Enables the `ssl`, `headers`, and `rewrite` modules for SSL support, HTTP headers manipulation, and URL rewriting.

#### **Secure Apache Settings**
```dockerfile
RUN echo "ServerTokens Prod" >> /etc/apache2/apache2.conf \
  && echo "ServerSignature Off" >> /etc/apache2/apache2.conf \
  && echo "TraceEnable Off" >> /etc/apache2/apache2.conf \
  && echo "Header always set Strict-Transport-Security \"max-age=31536000; includeSubDomains\"" >> /etc/apache2/apache2.conf \
  && echo "Header always set X-Content-Type-Options \"nosniff\"" >> /etc/apache2/apache2.conf \
  && echo "Header always set X-Frame-Options \"DENY\"" >> /etc/apache2/apache2.conf \
  && echo "Header always set X-XSS-Protection \"1; mode=block\"" >> /etc/apache2/apache2.conf \
  && echo "Header always set Content-Security-Policy \"default-src 'self';\"" >> /etc/apache2/apache2.conf \
  && echo "AllowEncodedSlashes NoDecode" >> /etc/apache2/apache2.conf \
  && echo "LogLevel warn" >> /etc/apache2/apache2.conf
```
- **Hardening Apache**: Configures Apache security headers and disables potentially dangerous settings:
    - Disables the `ServerTokens` and `ServerSignature` to hide the Apache version and reduce the information exposed about the server.
    - Configures strict HTTP security headers (`Strict-Transport-Security`, `X-Content-Type-Options`, etc.) to mitigate common attacks (e.g., clickjacking, cross-site scripting, etc.).
    - Disables HTTP TRACE method to prevent cross-site tracing attacks.

#### **SSL Configuration**
```dockerfile
RUN mkdir -p /etc/ssl/private && chmod 700 /etc/ssl/private \
    && mkdir -p /etc/ssl/certs && chmod 755 /etc/ssl/certs \
    && openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 \
    -keyout /etc/ssl/private/apache-selfsigned.key \
    -out /etc/ssl/certs/apache-selfsigned.crt \
    -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=localhost"
```
- **SSL certificate generation**: Creates a self-signed SSL certificate (`apache-selfsigned.crt`) and its private key (`apache-selfsigned.key`) using OpenSSL. These will be used for encrypting traffic over HTTPS.

#### **Apache Virtual Host Configuration for SSL**
```dockerfile
RUN echo "<VirtualHost *:443>" > /etc/apache2/sites-available/default-ssl.conf \
  && echo "    SSLEngine on" >> /etc/apache2/sites-available/default-ssl.conf \
  && echo "    SSLCertificateFile /etc/ssl/certs/apache-selfsigned.crt" >> /etc/apache2/sites-available/default-ssl.conf \
  && echo "    SSLCertificateKeyFile /etc/ssl/private/apache-selfsigned.key" >> /etc/apache2/sites-available/default-ssl.conf \
  && echo "    DocumentRoot /usr/src/network_trf_analyzer" >> /etc/apache2/sites-available/default-ssl.conf \
  && echo "    <Directory /usr/src/network_trf_analyzer>" >> /etc/apache2/sites-available/default-ssl.conf \
  && echo "        AllowOverride All" >> /etc/apache2/sites-available/default-ssl.conf \
  && echo "        Require all granted" >> /etc/apache2/sites-available/default-ssl.conf \
  && echo "    </Directory>" >> /etc/apache2/sites-available/default-ssl.conf \
  && echo "</VirtualHost>" >> /etc/apache2/sites-available/default-ssl.conf
```
- **SSL VirtualHost Configuration**: Configures Apache to serve traffic on HTTPS (port 443) with the self-signed SSL certificate created earlier. 
    - **DocumentRoot** is set to `/usr/src/network_trf_analyzer`, which is the directory containing the Python application.
    - **Directory settings** ensure that Apache can override configurations (`AllowOverride All`) and grant access (`Require all granted`).

#### **Enable SSL Site Configuration**
```dockerfile
RUN a2ensite default-ssl.conf
```
- **Enable SSL site**: Activates the SSL site configuration (`default-ssl.conf`) to ensure that Apache serves traffic securely over HTTPS.

#### **Restrict Access to Sensitive Directories**
```dockerfile
RUN echo "<Directory /usr/src/network_trf_analyzer>" > /etc/apache2/conf-available/

000-local.conf \
  && echo "    Require all denied" >> /etc/apache2/conf-available/000-local.conf \
  && echo "</Directory>" >> /etc/apache2/conf-available/000-local.conf
```
- **Restrict directory access**: Denies access to the directory `/usr/src/network_trf_analyzer` unless otherwise specified, enhancing security.

#### **Create .htpasswd for Basic Authentication**
```dockerfile
RUN htpasswd -cb /usr/src/network_trf_analyzer/.htpasswd user password \
  && echo "AuthType Basic" > /usr/src/network_trf_analyzer/.htaccess \
  && echo "AuthName \"Restricted Access\"" >> /usr/src/network_trf_analyzer/.htaccess \
  && echo "AuthUserFile /usr/src/network_trf_analyzer/.htpasswd" >> /usr/src/network_trf_analyzer/.htaccess \
  && echo "Require valid-user" >> /usr/src/network_trf_analyzer/.htaccess \
  && chmod 600 /usr/src/network_trf_analyzer/.htpasswd
```
- **Create `.htpasswd`**: Uses the `htpasswd` command to create a `.htpasswd` file containing user credentials (username and password) for basic authentication.
- **Configure `.htaccess`**: Sets up Basic Authentication using the `.htpasswd` file, requiring users to authenticate before accessing the application.

#### **Make GeoIP Script Executable**
```dockerfile
COPY geoip.sh ./
RUN chmod +x geoip.sh
```
- **Copy script**: Copies the `geoip.sh` script into the container and makes it executable.

#### **Set Permissions for Sensitive Files**
```dockerfile
RUN chmod -R 750 /usr/src/network_trf_analyzer
```
- **Set permissions**: Ensures that the application files have the appropriate permissions, allowing access only to necessary users.

---

## Conclusion

This Dockerfile creates a secure, production-ready image for serving a Python-based web application with Apache using SSL and Basic Authentication. It follows security best practices like:
- Running the application as a non-root user.
- Enabling SSL encryption to ensure secure data transmission.
- Configuring Apache to minimize exposed information and harden the server's security.
