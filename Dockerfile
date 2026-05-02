# Imagem base com Python
FROM python:3.11-slim

# Instala o Tesseract e o idioma português no servidor
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-por \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Copia e instala as dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do projeto
COPY . .

# Porta que o app vai usar
EXPOSE 8000

# Comando para rodar o app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]