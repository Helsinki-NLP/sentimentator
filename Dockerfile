FROM python:alpine

WORKDIR /app

COPY . /app 
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

RUN python3 data_import.py en data/en/en.txt data/en/ids.txt
RUN python3 test_data_import.py en data/en_test/TOMATSsentimentator_split.txt data/en/ids.txt
ENTRYPOINT ["python", "main.py"]
