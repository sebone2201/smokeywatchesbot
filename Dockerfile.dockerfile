FROM python:3.11-slim

# Evita interattività e aggiorna il sistema
ENV DEBIAN_FRONTEND=noninteractive

# Installa dipendenze di sistema
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium \
    curl \
    unzip \
    gnupg \
    wget \
    fonts-liberation \
    libnss3 \
    libatk-bridge2.0-0 \
    libxss1 \
    libgtk-3-0 \
    libasound2 \
    libgbm1 \
    libxshmfence1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Imposta variabili d'ambiente per Selenium
ENV CHROME_BIN=/usr/bin/chromium
ENV PATH=$PATH:/usr/bin/chromium

# Crea directory app
WORKDIR /app

# Copia i file
COPY . .

# Installa le dipendenze Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Comando di avvio
CMD ["python3", "main.py"]
