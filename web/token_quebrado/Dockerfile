FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir flask==3.0.3
COPY app/ /app/
ENV FLAG="CITT{jwt_alg_none_es_peligroso}"
EXPOSE 5000
CMD ["python", "app.py"]
