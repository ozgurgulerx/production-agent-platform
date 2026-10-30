# AgentCore Runtime images must be linux/arm64 (B2). Build with: docker buildx build --platform linux/arm64 ...
FROM --platform=linux/arm64 python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
ENV PYTHONUNBUFFERED=1 AWS_REGION=us-east-1
EXPOSE 8080
# ADOT auto-instrumentation turns Strands spans into CloudWatch GenAI Observability traces (H1)
CMD ["opentelemetry-instrument", "python", "main.py"]
