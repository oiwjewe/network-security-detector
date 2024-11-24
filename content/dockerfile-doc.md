# Technical Documentation for Dockerfile

This Dockerfile outlines the steps necessary to build a Docker container that runs a Python application with an Apache web server, configured for secure SSL communication and directory protection. Each section of the Dockerfile is explained below.

---

### 1. **Base Image**
```dockerfile
FROM python:3.11
```
- **Purpose**: Specifies the base image for the Docker container. In this case, it uses the official Python 3.11 image, which includes a Python runtime environment. This is essential for running Python-based applications.
- **Explanation**: The image contains Python and other essential tools for Python development, and is built on top of a Debian-based distribution.

---

### 2. **Set Working Directory**
```dockerfile
WORKDIR /usr/src/network_trf_analyzer
```
- **Purpose**: Sets the working directory inside the container to `/usr/src/network_trf_analyzer`.
- **Explanation**: All subsequent commands will be executed from this directory. This is where the Python application and other files will be located.

---

### 3. **Install System Dependencies**
```dockerfile
RUN apt-get update && apt-get install -y \
    apache2 \
    apache2-utils \
    ssl-cert \
    python3-distutils \
    python3-setuptools \
    python3-pip \
    build-essential \
    wget \
    tar \
  && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*
```
- **Purpose**: Updates the package list and installs a variety of system dependencies necessary for running Apache, Python, SSL support, and the building of Python packages.
- **Explanation**:
  - `apache2`: Installs Apache web server.
  - `apache2-utils`: Provides utilities for Apache, such as `htpasswd`.
  - `ssl-cert`: Provides SSL utilities.
  - `python3-distutils`, `python3-setuptools`, `python3-pip`: Install tools for managing Python packages and dependencies.
  - `build-essential`: Installs packages necessary for compiling and building software.
  - `wget`, `tar`: Install tools for downloading and extracting files.
  - The `apt-get autoremove` and `rm -rf /var/lib/apt/lists/*` clean up unnecessary files to reduce image size.

---

### 4. **Disable Apache Modules**
```dockerfile
RUN a2dismod -f status && a2dismod -f autoindex
```
- **Purpose**: Disables the `status` and `autoindex` Apache modules to improve security by reducing potential attack surfaces.
- **Explanation**: 
  - `status`: This module provides a web interface for Apache server status, which could leak sensitive information.
  - `autoindex`: Disables the automatic directory listing feature to prevent exposing directory contents.

---

### 5. **Enable Necessary Apache Modules**
```dockerfile
RUN a2enmod ssl headers rewrite
```
- **Purpose**: Enables essential Apache modules for security and functionality.
- **Explanation**:
  - `ssl`: Enables SSL (Secure Sockets Layer) support for encrypted communication.
  - `headers`: Allows the manipulation of HTTP headers for security settings.
  - `rewrite`: Enables URL rewriting, which can be useful for routing or redirecting traffic securely.

---

### 6. **Configure Apache for Secure Settings**
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
- **Purpose**: Configures Apache with secure settings to mitigate common web vulnerabilities.
- **Explanation**:
  - `ServerTokens Prod`: Limits the information Apache sends in response headers.
  - `ServerSignature Off`: Prevents Apache from showing detailed version information in error pages.
  - `TraceEnable Off`: Disables the TRACE HTTP method to prevent potential cross-site tracing attacks.
  - HTTP headers such as `Strict-Transport-Security`, `X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`, and `Content-Security-Policy` are set for enhanced security (e.g., preventing cross-site scripting and clickjacking).
  - `AllowEncodedSlashes NoDecode`: Prevents URL decoding for security reasons.
  - `LogLevel warn`: Sets the Apache logging level to warn, minimizing unnecessary log verbosity.

---

### 7. **Enable HTTPS and Configure SSL Directories**
```dockerfile
RUN mkdir -p /etc/ssl/private && \
    chmod 700 /etc/ssl/private && \
    mkdir -p /etc/ssl/certs && \
    chmod 755 /etc/ssl/certs
```
- **Purpose**: Creates the directories for storing SSL certificates and sets proper permissions.
- **Explanation**: 
  - `/etc/ssl/private`: Directory for storing private SSL keys with restricted permissions.
  - `/etc/ssl/certs`: Directory for storing public SSL certificates.

---

### 8. **Generate Self-Signed SSL Certificate**
```dockerfile
RUN openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 \
    -keyout /etc/ssl/private/apache-selfsigned.key \
    -out /etc/ssl/certs/apache-selfsigned.crt \
    -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=localhost"
```
- **Purpose**: Generates a self-signed SSL certificate.
- **Explanation**: A self-signed certificate is useful for development or testing environments but should not be used in production. The `openssl` command creates a 2048-bit RSA key pair and a certificate valid for 365 days.

---

### 9. **Configure SSL in Apache**
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
- **Purpose**: Configures Apache to use the self-signed SSL certificate for HTTPS communication.
- **Explanation**:
  - The `<VirtualHost *:443>` block configures Apache to listen on port 443 (HTTPS).
  - `SSLEngine on`: Enables SSL for this virtual host.
  - `SSLCertificateFile` and `SSLCertificateKeyFile`: Point to the self-signed certificate and private key created earlier.
  - Configures the document root for the web server to the working directory and applies directory-level permissions.

---

### 10. **Enable SSL Site Configuration**
```dockerfile
RUN a2ensite default-ssl.conf
```
- **Purpose**: Enables the default SSL site configuration in Apache.
- **Explanation**: Ensures Apache uses the SSL configuration we just set up.

---

### 11. **Create .htaccess File for Directory Protection**
```dockerfile
RUN echo "AuthType Basic" > /usr/src/network_trf_analyzer/.htaccess \
  && echo "AuthName \"Restricted Access\"" >> /usr/src/network_trf_analyzer/.htaccess \
  && echo "AuthUserFile /usr/src/network_trf_analyzer/.htpasswd" >> /usr/src/network_trf_analyzer/.htaccess \
  && echo "Require valid-user" >> /usr/src/network_trf_analyzer/.htaccess
```
- **Purpose**: Sets up basic HTTP authentication for access control to the application directory.
- **Explanation**: 
  - `AuthType Basic`: Specifies basic HTTP authentication.
  - `AuthName`: Defines the realm for authentication.
  - `AuthUserFile`: Points to the `.htpasswd` file (which contains username and password).
  - `Require valid-user`: Ensures only authenticated users can access the directory.

---

### 12. **Secure Sensitive Directories

**
```dockerfile
RUN echo "<Directory /usr/src/network_trf_analyzer>" > /etc/apache2/conf-available/000-local.conf \
  && echo "    Require all denied" >> /etc/apache2/conf-available/000-local.conf \
  && echo "</Directory>" >> /etc/apache2/conf-available/000-local.conf
```
- **Purpose**: Restricts access to sensitive directories.
- **Explanation**: Ensures that no unauthorized user can access the specified directory.

---

### 13. **Enable Local Directory Restrictions**
```dockerfile
RUN a2enconf 000-local
```
- **Purpose**: Applies the local directory restriction configuration to Apache.

---

### 14. **Copy and Make the geoip.sh Script Executable**
```dockerfile
COPY geoip.sh ./
RUN chmod +x geoip.sh
```
- **Purpose**: Copies the `geoip.sh` script into the container and makes it executable.
- **Explanation**: This script is part of the application setup and is executed when the container starts.

---

### 15. **Set Entry Point and Start Apache**
```dockerfile
ENTRYPOINT ["bash", "/usr/src/network_trf_analyzer/geoip.sh"]
CMD service apache2 start && tail -f /dev/null
```
- **Purpose**: Defines the entry point and start command for the container.
- **Explanation**:
  - `ENTRYPOINT`: Executes the `geoip.sh` script when the container starts.
  - `CMD`: Starts the Apache server in the background and keeps the container running with `tail -f /dev/null`.

---

This Dockerfile ensures that the container is configured for a secure, Apache-backed, Python application with HTTPS support and access control, making it suitable for both development and production environments.
