FROM python:3.11-slim-bookworm

WORKDIR /app

# -----------------------------------------------------
# Install Microsoft ODBC Driver 18 for SQL Server
# -----------------------------------------------------

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl \
       ca-certificates \
       gnupg \
       unixodbc \
       unixodbc-dev \
    && curl -sSL -O https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb \
    && dpkg -i packages-microsoft-prod.deb \
    && rm packages-microsoft-prod.deb \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
       msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*


# -----------------------------------------------------
# Install Python dependencies
# -----------------------------------------------------

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir --upgrade \
       setuptools \
       wheel \
       msgpack==1.2.1


# -----------------------------------------------------
# Copy application
# -----------------------------------------------------

COPY . .


# -----------------------------------------------------
# Backend port
# -----------------------------------------------------

EXPOSE 4000


# -----------------------------------------------------
# Start FastAPI
# -----------------------------------------------------

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000"]