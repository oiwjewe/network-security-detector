import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.neural_network import MLPRegressor
import joblib
import geoip2.database
import numpy as np
import os
from datetime import datetime

# Função para salvar figuras geradas
def save_figure(figure, file_name):
    """Função para salvar figuras geradas pelo matplotlib."""
    figure.savefig(file_name)
    print(f"Figura salva em: {file_name}")

# Função para salvar detecções estruturadas em CSV
def save_detection_to_csv(detections, filename='detecções_network_traffic.csv'):
    """Função para salvar detecções em um arquivo CSV."""
    df = pd.DataFrame(detections)
    df.to_csv(filename, index=False)
    print(f"Detecções salvas em: {filename}")

# Função para salvar mensagens de detecção em um arquivo TXT
def save_detection_to_txt(detection_message, filename='detecções_network_traffic.txt'):
    """Função para salvar mensagens de detecção em um arquivo TXT."""
    with open(filename, 'a') as file:
        file.write(detection_message + '\n')
    print(f"Mensagem salva em: {filename}")

# Função para carregar o modelo de machine learning previamente treinado
def load_trained_model(model_filename='anomaly_model.pkl'):
    """Função para carregar o modelo de machine learning previamente treinado."""
    return joblib.load(model_filename)

# Função para aplicar políticas de segurança e bloquear IPs de alto risco
def enforce_security_policy(risk_scores, data, threshold=0.5):
    """Aplica políticas de segurança para bloquear ou alertar sobre IPs de alto risco com base em pontuação."""
    risky_ips = []
    for i, score in enumerate(risk_scores):
        if score > threshold:  # Se a pontuação de risco for maior que o limiar, bloqueamos o IP
            ip = data[i]['ip']
            risky_ips.append(ip)
            # Adiciona a funcionalidade de bloqueio
            save_blocked_ip(ip)
    return risky_ips

# Função para salvar IPs bloqueados em um arquivo (simulação de bloqueio)
def save_blocked_ip(ip, filename='blocked_ips.txt'):
    """Função para salvar IPs bloqueados em um arquivo de texto."""
    with open(filename, 'a') as file:
        file.write(ip + '\n')
    print(f"IP bloqueado: {ip} (salvo em {filename})")

# Função para análise e detecção de tráfego de rede
def analyze_and_detect_traffic(data, geoip_reader, model):
    """Função para análise e detecção de tráfego de rede."""
    
    detections = []  # Lista para armazenar detecções para salvar no CSV
    detection_messages = []  # Lista para mensagens de texto simples
    risk_scores = []  # Lista para armazenar as pontuações de risco

    # 1. Geolocation-Based Threat Detection
    for entry in data:
        ip = entry['ip']
        try:
            response = geoip_reader.city(ip)
            country = response.country.iso_code
            if country in ['RU', 'CN', 'KP']:  # Países de risco
                detection_message = f"Alerta: IP {ip} originário de um país de risco ({country})"
                detection_messages.append(detection_message)
                detections.append({"ip": ip, "detecção": "Geolocation Threat", "country": country})
                risk_scores.append(0.9)  # Alto risco devido à geolocalização
            else:
                risk_scores.append(0.2)  # Baixo risco
        except geoip2.errors.GeoIP2Error:
            pass  # Se o IP não puder ser localizado, ignoramos

    # 2. Anomaly Detection with Machine Learning (Isolation Forest)
    for entry in data:
        feature_data = entry['features']  # AQUI deve ser as features usadas no modelo de ML
        score = model.predict([feature_data])  # Prevendo com o modelo treinado
        scores = score[0]  # Armazenando o resultado da predição
        
        if score[0] == -1:  # -1 indica anomalia detectada pelo modelo Isolation Forest
            detection_message = f"Alerta: IP {entry['ip']} identificado com comportamento anômalo."
            detection_messages.append(detection_message)
            detections.append({"ip": entry['ip'], "detecção": "Anomalia", "score": scores})
            risk_scores.append(0.8)  # Alto risco por anomalia detectada
        else:
            risk_scores.append(0.1)  # Baixo risco

    # 3. Aplicando as políticas de segurança (bloqueando IPs de alto risco)
    risky_ips = enforce_security_policy(risk_scores, data)
    if risky_ips:
        print(f"IPs de alto risco detectados e bloqueados: {risky_ips}")

    # 4. Salvando as Detecções e Mensagens
    if detections:
        save_detection_to_csv(detections, filename="detecções_network_traffic.csv")
    if detection_messages:
        for message in detection_messages:
            save_detection_to_txt(message, filename="detecções_network_traffic.txt")

    # 5. Salvando Gráficos
    fig, ax = plt.subplots()
    ax.plot(risk_scores)
    ax.set_title('Anomalias Detectadas no Tráfego de Rede')
    save_figure(fig, "detecção_anomalias.png")  # Salvando a imagem gerada

# Função de carregamento de dados para demonstração
def load_sample_data():
    """Função para carregar dados de exemplo"""
    return [
        {"ip": "192.168.1.1", "features": [0.5, 1.2, 0.3]},
        {"ip": "203.0.113.5", "features": [1.1, 0.9, 0.7]},
        {"ip": "10.0.0.1", "features": [0.8, 1.5, 0.6]}
    ]

# Exemplo de como carregar o modelo e executar a análise
if __name__ == "__main__":
    # Carregando os dados de tráfego
    data = load_sample_data()

    # Inicializando o leitor de GeoIP (para geolocalização)
    geoip_reader = geoip2.database.Reader('/path/to/GeoLite2-City.mmdb')

    # Carregando o modelo de Machine Learning previamente treinado
    model = load_trained_model('anomaly_model.pkl')

    # Analisando e detectando tráfego
    analyze_and_detect_traffic(data, geoip_reader, model)
