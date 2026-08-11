FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# Install application dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Patch packages identified by the Trivy image scan.
RUN pip install --no-cache-dir --upgrade \
    setuptools==78.1.1 \
    wheel==0.46.2 \
    jaraco.context==6.1.0 \
    msgpack==1.2.1

COPY . .

EXPOSE 4000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000"]
