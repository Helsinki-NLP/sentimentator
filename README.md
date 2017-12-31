
# sentimentator

*Sentimentator* is a tool for creating fine-grained sentence-level annotations
for research in *Sentiment Analysis*. Annotations are needed for compiling data
sets for machine learning tasks.

## Usage

### With docker

Getting *sentimentator* up and running should be straightforward with Docker.
After building the image, run it and expose port 5000. Example assumes your
image is called `sentimentator`:

    docker run -d -p 5000:5000 sentimentator

Or if you wish to receive logs to your terminal:

    docker run -it --rm -p 5000:5000 sentimentator

#### Test data

Initially the database is empty. You can populate it with test data by
executing database initiation script in a running container:

    docker exec -it <container_name> python /app/init_db.py
