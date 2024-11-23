<h3>Description:</h3>


<h3>Usage:</h3>

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


<h3>Considerations:</h3>

This script were developed as result of a hacker challenge for a job interview, so it won’t be perfect. It’s not designed to be perfect, but to be flexible so it could be improved over time.<br> 
Feel free to study it and adapt it into your reality if it makes sense to you.<br> 

*I do not recommend or suggest to use this script as it is in real environments, once it was not fully tested and may lead to impacts in the network, such internal IP blocks while AI is learning.*<br> 
*It’s dedicate to study only! I won’t accept responsibilities for any damage caused  by it’s irresponsible or illegal use.*<br> 
*Do not run it in networks where you don’t have express and legal consent.*<br> 
Commercial use of this script is not recommended once it was developed with help of ChatGPT.

<h3>Acknowledgments</h3>
I'm really thankfull for this team that with only a request made my mind expand and grow in so many directions in such a little time.<br> 
I really appreciated and enjoyed this experience.<br> 
I want more. I'm hungry to be part of the pack!

