
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
executing the database initiation script in a running container.
Usage:

    docker exec -it <container_name> python /app/data_import.py <lang_name> <lang_filename> <alignment_filename>

**<lang_name>**: two-letter language code, for example *en*, *fi*, or *sv*.
**<lang_filename>**: name of the .txt file from which to import each line as a sentence to the database.
**<alignment_filename>**: name of the .txt file from which to import the OPUS metadata for each sentence. The *data_import.py* script imports metadata for a pivot language by extracting the sentence id and the path to the OPUS document id for each sentence from the parallel line in the alignment file.
Example alignment file:

    # en/0/3509138/6031634.xml.gz	fi/0/3509138/6003289.xml.gz	5	3
    # en/0/3509138/6031634.xml.gz	fi/0/3509138/6003289.xml.gz	6	4
    # en/0/3509138/6031634.xml.gz	fi/0/3509138/6003289.xml.gz	9	6
    [...]

OPUS parallel corpus files are available for download at http://opus.nlpl.eu/OpenSubtitles2018.php in the MOSES/GIZA++ format.
