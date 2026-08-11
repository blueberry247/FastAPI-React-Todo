FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# Install dependencies and security updates in one layer
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir --upgrade \
       setuptools \
       wheel \
       msgpack==1.2.1

COPY . .

EXPOSE 4000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000"]