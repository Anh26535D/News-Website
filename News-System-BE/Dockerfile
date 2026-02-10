FROM python:3.12-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/install/bin:$PATH" \
    PYTHONPATH="/install/lib/python3.12/site-packages:$PYTHONPATH"

WORKDIR /app

COPY --from=builder /install /install

COPY . .

RUN sed -i 's/\r$//' run.sh && \
    chmod +x run.sh && \
    useradd -m nonroot && \
    chown -R nonroot:nonroot /app

USER nonroot

EXPOSE 8000

ENTRYPOINT ["./run.sh"]