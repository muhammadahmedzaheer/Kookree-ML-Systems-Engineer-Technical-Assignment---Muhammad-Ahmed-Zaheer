# ---------- Stage 1: Builder ----------
FROM python:3.11-slim AS builder

WORKDIR /app

# Install dependencies required for building and OpenCV
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --prefix=/install -r requirements.txt


# ---------- Stage 2: Runtime ----------
FROM python:3.11-slim

WORKDIR /app

# 👇 Required again here because libgl1 is NOT shared from builder
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local
COPY . .

EXPOSE 50051

CMD ["python", "server.py"]