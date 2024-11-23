<h3>Description:</h3>


<h3>Usage:</h3>

To run this script, you will need to use the Docker image available in Docker Hub. For this, follow the instructions bellow.

For other distributions and systems or troubleshooting errors that may occur during Docker installation in your environment, please refer to the official Docker documentation at https://docs.docker.com/get-docker/


<p style="font-style:italic;">Run the commands bellow in your terminal. If Docker is already installed in your environment, skip to step 5:</p>


#1)Check if Docker is installed: 
<p style="font-style:italic;">docker --version</p>

#2)Check Docker service status: 
<p style="font-style:italic;">sudo systemctl status docker</p>

#3)Update packages: 
<p style="font-style:italic;">sudo apt update && apt upgrade -y && apt autoremove</p>

#4)Install Docker: 
<p style="font-style:italic;">sudo apt install docker.io docker-compose</p>

#5)Download the Docker image:
<p style="font-style:italic;">sudo docker pull network-security-detector:latest></p>

#6)See the Docker images available in your environment: 
<p style="font-style:italic;">sudo docker images</p>

#7)Build the image:
<p style="font-style:italic;">sudo docker build -t network-security-detector .</p>

#8)Finally, to run the script, simply execute the following command:
<p style="font-style:italic;">sudo docker run --rm network-security-detector:latest python3 ./network_trf_analyzer.py</p>


#or RUN IN BACKGROUND:
<p style="font-style:italic;">sudo docker run -d --name network-security-detector-container network-security-detector</p>


<h3>Considerations:</h3>

This script were developed as result of a hacker challenge for a job interview, so it won’t be perfect. It’s not designed to be perfect, but to be flexible so it could be improved. 

Feel free to study it and adapt it into your reality if it makes sense to you.

<p style="font-style:italic;">I do not recommend or suggest to use this script as it is in real environments, once it was not fully tested and may lead to impacts in the network, such internal IP blocks while AI is learning.

It’s dedicate to study only! I won’t accept responsibilities for any damage caused  by it’s irresponsible or illegal use.

Do not run it in networks where you don’t have express and legal consent.</p>

Commercial use of this script is not recommended once it was developed with help of Chat GPT.
