# Use uma imagem oficial do Python como base
FROM python:3.9-slim

# Atualizar e instalar dependências necessárias para OpenCV
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libglib2.0-0 && \
    apt-get clean

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar os arquivos de requirements
COPY requirements.txt .

# Instalar dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código para o diretório /app
COPY . .

# Comando para executar o script principal
CMD ["python", "main.py"]
