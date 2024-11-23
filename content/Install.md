<h3>Installation and Usage:</h3>

To run this script, you’ll need to use the Docker image available on Docker Hub. Follow the instructions below for Debian-based Linux distributions. For other Linux distributions, operating systems, or if you encounter any issues during Docker installation, please refer to the official Docker documentation at https://docs.docker.com/get-docker/

*Run the commands bellow in your terminal. If Docker is already installed in your environment, skip to step 5:*

#1)Check if Docker is installed:<br> 
*docker --version*

#2)Check Docker service status:<br> 
*sudo systemctl status docker*
#3)Update packages:<br> 
*sudo apt update && apt upgrade -y && apt autoremove*

#4)Install Docker:<br> 
*sudo apt install docker.io docker-compose*

#5)Download the Docker image:<br>
*sudo docker pull network-security-detector:latest>*

#6)See the Docker images available in your environment:<br> 
*sudo docker images*

#7)Build the image:<br>
*sudo docker build -t network-security-detector .*

#8)Finally, to run the script, simply execute the following command:<br>
*sudo docker run --rm network-security-detector:latest python3 ./network_trf_analyzer.py*


#or RUN IN BACKGROUND:<br>
*sudo docker run -d --name network-security-detector-container network-security-detector*