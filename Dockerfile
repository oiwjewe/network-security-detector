FROM python:latest

WORKDIR /usr/src/network_trf_analyzer

RUN sudo apt update && apt upgrade -y && apt autoremove

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./network_trf_analyzer.py" ]


