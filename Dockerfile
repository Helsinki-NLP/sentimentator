FROM python:alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY sentimentator/ sentimentator/
COPY main.py .

EXPOSE 5000

ENTRYPOINT ["python", "main.py"]
