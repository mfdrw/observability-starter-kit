FROM python:3.12-slim
RUN pip install --no-cache-dir requests
COPY traffic_generator.py /app/traffic_generator.py
CMD ["python", "/app/traffic_generator.py"]