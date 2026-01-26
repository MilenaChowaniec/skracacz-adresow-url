FROM python:3.11-slim AS base

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS production

COPY . .

RUN pip install --no-cache-dir pytest pytest-cov

EXPOSE 5000

CMD ["python", "run.py"]