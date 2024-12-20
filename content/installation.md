<h3>Installation:</h3><br>

To run this script, you’ll need to use the Docker image available on Docker Hub. Follow the instructions below for Debian-based Linux distributions. For other Linux distributions, operating systems, or if you encounter any issues during Docker installation, please refer to the official Docker documentation at https://docs.docker.com/get-docker/

*Run the commands bellow in your terminal. If Docker is already installed in your environment, skip to step 5:*<br>

1)Check if Docker is installed:<br> 

`docker --version` 

*If it returns nothing, then skip step 2*<br>
*If it returns the version, skip step 4*

2)Check Docker service status:<br> 

`sudo systemctl status docker` , if it's disable, then enable/start with: `sudo systemctl enable --now docker`

3)Update packages:<br> 

`sudo apt update && apt upgrade -y && apt autoremove`

4)Install Docker:<br> 

`sudo apt install docker.io docker-compose`

5)Download the Docker image:<br>

`sudo docker pull w1ndx/network-traffic-analyzer:first`

6)See the Docker images available in your environment:<br> 

`sudo docker images`

7)Build the image:<br>

`sudo docker build -t w1ndx/network-traffic-analyzer:first .`

