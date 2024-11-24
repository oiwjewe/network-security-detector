# Stage 1: Build environment (to install dependencies)
FROM python:3.11-slim as build

# Install dependencies needed for building (e.g., build tools, wget, tar)
RUN apt-get update && apt-get install -y build-essential wget tar \
    && apt-get clean

# Set working directory for build stage
WORKDIR /usr/src/network_trf_analyzer

# Copy necessary files into the build stage (ensure these files exist in your build context)
COPY . .

# Stage 2: Final image (runtime environment)
FROM python:3.11-slim

# Install runtime dependencies, including Apache, SSL support, and Python packages
RUN apt-get update && apt-get install -y \
    apache2 \
    apache2-utils \
    ssl-cert \
    python3-pip \
    && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /usr/src/network_trf_analyzer

# Install Python dependencies from requirements.txt
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Disable unnecessary Apache modules to reduce attack surface (run as root)
RUN a2dismod -f status && a2dismod -f autoindex

# Enable necessary Apache modules (SSL, headers, rewrite) (run as root)
RUN a2enmod ssl headers rewrite

# Secure Apache settings by disabling server signature, restricting trace, and adding security headers
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

# Enable HTTPS and configure SSL
RUN mkdir -p /etc/ssl/private && chmod 700 /etc/ssl/private \
    && mkdir -p /etc/ssl/certs && chmod 755 /etc/ssl/certs \
    && openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 \
    -keyout /etc/ssl/private/apache-selfsigned.key \
    -out /etc/ssl/certs/apache-selfsigned.crt \
    -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=localhost"

# Configure SSL for Apache
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

# Enable the SSL site configuration
RUN a2ensite default-ssl.conf

# Secure sensitive directories by restricting access
RUN echo "<Directory /usr/src/network_trf_analyzer>" > /etc/apache2/conf-available/000-local.conf \
  && echo "    Require all denied" >> /etc/apache2/conf-available/000-local.conf \
  && echo "</Directory>" >> /etc/apache2/conf-available/000-local.conf

# Enable the local directory restrictions
RUN a2enconf 000-local

# Create .htpasswd file using htpasswd and secure the .htaccess file
RUN htpasswd -cb /usr/src/network_trf_analyzer/.htpasswd user password \
  && echo "AuthType Basic" > /usr/src/network_trf_analyzer/.htaccess \
  && echo "AuthName \"Restricted Access\"" >> /usr/src/network_trf_analyzer/.htaccess \
  && echo "AuthUserFile /usr/src/network_trf_analyzer/.htpasswd" >> /usr/src/network_trf_analyzer/.htaccess \
  && echo "Require valid-user" >> /usr/src/network_trf_analyzer/.htaccess \
  && chmod 600 /usr/src/network_trf_analyzer/.htpasswd

# Copy and set permissions for the geoip.sh script
COPY geoip.sh ./
RUN chmod +x geoip.sh

# Set proper permissions on the working directory and sensitive files
RUN chmod -R 750 /usr/src/network_trf_analyzer

# Default command to run Apache in the background and then the Python script after Apache is up
ENTRYPOINT ["bash", "-c", "/usr/src/network_trf_analyzer/geoip.sh && service apache2 start && python3 /usr/src/network_trf_analyzer/network_trf_analyzer.py"]

# Start Apache in the foreground to keep the container running
CMD ["apache2ctl", "-D", "FOREGROUND"]
