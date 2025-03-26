FROM python:alpine

WORKDIR /app

COPY . /app 
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# run the following command to import default EN data to DB
RUN python3 data_import.py en data/en/en.txt data/en/ids.txt
# run the following command to import test data to DB
RUN python3 test_data_import.py en data/en_test/TOMATSsentimentator_split.txt data/en/ids.txt
ENTRYPOINT ["python", "main.py"]
