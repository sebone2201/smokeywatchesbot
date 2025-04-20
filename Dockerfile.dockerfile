FROM python:3.11-slim

# Evita problemi con interazione
ENV DEBIAN_FRONTEND=noninteractive

# Installa dipendenze e Google Chrome
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libxss1 \                     # <-- Aggiungi questo
    libxtst6 \                   # <-- E questo
    libglib2.0-0 \               # <-- E questo
    libu2f-udev \    
    xdg-utils \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*
   


# Aggiunge repository ufficiale di Chrome e lo installa
RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

RUN google-chrome --version


# Installa le dipendenze Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il tuo codice
COPY . /opt/render/project/src
WORKDIR /opt/render/project/src

# Avvia lo script
CMD ["python3", "main.py"]
