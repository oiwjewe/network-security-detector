<h3>Installation and Usage:</h3><br>

To run this script, you’ll need to use the Docker image available on Docker Hub. Follow the instructions below for Debian-based Linux distributions. For other Linux distributions, operating systems, or if you encounter any issues during Docker installation, please refer to the official Docker documentation at https://docs.docker.com/get-docker/

*Run the commands bellow in your terminal. If Docker is already installed in your environment, skip to step 5:*<br>

#1)Check if Docker is installed:<br> 
<prev>docker --version</prev>

#2)Check Docker service status:<br> 
<prev>sudo systemctl status docker</prev>

#3)Update packages:<br> 
<prev>sudo apt update && apt upgrade -y && apt autoremove</prev>

#4)Install Docker:<br> 
<prev>sudo apt install docker.io docker-compose</prev>

#5)Download the Docker image:<br>
<prev>sudo docker pull w1ndx/network-traffic-analyzer:first</prev>

#6)See the Docker images available in your environment:<br> 
<prev>sudo docker images</prev>

#7)Build the image:<br>
<prev>sudo docker build -t w1ndx/network-traffic-analyzer:first .</prev>

#8)Finally, to run the script, simply execute the following command:<br>
<prev>sudo docker run --rm w1ndx/network-traffic-analyzer:first python3 ./network_trf_analyzer.py</prev>
