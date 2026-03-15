FROM python:3.9-slim
WORKDIR /app
COPY src/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
WORKDIR /app/src
CMD ["flask", "--app", "app.py", "run", "--host=0.0.0.0", "--port=5001"]
