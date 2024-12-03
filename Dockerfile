# Imagem base
FROM python:3.9-slim

# Diretório de trabalho
WORKDIR /app

# Copiar dependências
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Comando padrão
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.enableCORS=false"]
