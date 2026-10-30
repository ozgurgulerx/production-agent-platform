# Hosted agents run on linux/amd64. Build with: docker build --platform linux/amd64 -t ticket-agent-hosted:1 .
FROM python:3.13-slim
ENV PYTHONNOUSERSITE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
EXPOSE 8088
CMD ["python", "main.py"]
