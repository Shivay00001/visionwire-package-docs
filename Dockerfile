FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || true
COPY . .
ENTRYPOINT ["python", "visionwire_universal_app.py"]
