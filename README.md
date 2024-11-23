<h3>Description:</h3>


<h3>Usage:</h3>

To run this script, you will need to use the Docker image available in Docker Hub. For this, follow the instructions bellow.

For other distributions and systems or troubleshooting errors that may occur during Docker installation in your environment, please refer to the official Docker documentation at https://docs.docker.com/get-docker/


Run the commands bellow in your terminal. If Docker is already installed in your environment, skip to step 5:


#1)Check if Docker is installed: 
docker --version

#2)Check Docker service status: 
sudo systemctl status docker

#3)Update packages: 
sudo apt update && apt upgrade -y && apt autoremove

#4)Install Docker: 
sudo apt install docker.io docker-compose

#5)Download the Docker image:
sudo docker pull <network-security-detector:tag>

#6)See the Docker images available in your environment: 
sudo docker images

#7)Build the image:
sudo docker build -t network-security-detector .

#8)Finally, to run the script, simply execute the following command:
sudo docker run --rm <network-security-detector:tag> python3 ./network_trf_analyzer


#or RUN IN BACKGROUND:
sudo docker run -d --name network-security-detector-container network-security-detector


<h3>Considerations:</h3>

This script were developed as result of a hacker challenge for a job interview, so it won’t be perfect. It’s not designed to be perfect, but to be flexible so it could be improved. 

Feel free to study it and adapt it into your reality if it makes sense to you.

I do not recommend or suggest to use this script as it is in real environments, once it was not fully tested and may lead to impacts in the network, such internal IP blocks while AI is learning.

It’s dedicate to study only! I won’t accept responsibilities for any damage caused  by it’s irresponsible or illegal use.

Do not run it in networks where you don’t have express and legal consent.

Commercial use of this script is not recommended once it was developed with help of Chat GPT.
