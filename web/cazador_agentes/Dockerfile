FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir flask==3.0.3
COPY app/ /app/
ENV FLAG="CITT{el_user_agent_te_delata}"
EXPOSE 5000
CMD ["python", "app.py"]
