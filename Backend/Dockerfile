FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# Upgrade Python packaging tools to patched versions.
RUN pip install --no-cache-dir --upgrade \
    pip \
    setuptools \
    wheel==0.46.2 \
    jaraco.context==6.1.0

# Install application dependencies.
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 4000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000"]
