FROM python:3.10.8-slim-buster
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpq-dev 
RUN python -m pip install .
EXPOSE 8000
