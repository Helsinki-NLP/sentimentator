
# sentimentator

*Sentimentator* is a tool for creating fine-grained sentence-level annotations
for research in *Sentiment Analysis*. Annotated sentences are needed to compile
comprehensive data sets for tasks such as machine learning.

## Usage

### With docker

Getting *sentimentator* up and running should be straightforward with Docker.
After building the image, run it and expose port 5000. Example assumes your
image is called `sentimentator`:

    docker run -d -p 5000:5000 sentimentator

#### Test data

Initially the database is empty. You can populate it with test data by
executing database initiation script in a running container:

    docker exec -it <container_name> python /app/init_db.py
