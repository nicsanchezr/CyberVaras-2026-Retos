FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir flask==3.0.3
COPY app/ /app/
# La flag vive como archivo fuera del webroot, objetivo del LFI.
ARG FLAG="CITT{lfi_hasta_la_raiz}"
RUN echo "$FLAG" > /flag.txt
EXPOSE 5000
CMD ["python", "app.py"]
