FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    chromium \
    chromium-driver \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set env var so Chrome works
ENV CHROME_BIN=/usr/bin/chromium

# Copy project
WORKDIR /app
COPY . .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Run app
CMD ["python3", "main.py"]
