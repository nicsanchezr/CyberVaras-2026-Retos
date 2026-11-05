FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir flask==3.0.3 lxml==5.3.0
COPY app/ /app/
# La flag se lee por XXE desde un archivo local del contenedor.
ARG FLAG="CITT{xxe_entidades_externas}"
RUN echo "$FLAG" > /flag.txt
EXPOSE 5000
CMD ["python", "app.py"]
