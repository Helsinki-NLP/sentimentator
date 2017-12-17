FROM python:alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY static/ static/
COPY templates/ templates/
COPY init_db.py .
COPY models.py .
COPY senti.py .

RUN chmod 0755 senti.py

EXPOSE 5000

ENTRYPOINT ["./senti.py"]
