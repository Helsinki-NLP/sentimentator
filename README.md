
# sentimentator

*Sentimentator* is a tool for creating fine-grained sentence-level annotations
for research in *Sentiment Analysis*. Annotations are needed for compiling data
sets for machine learning tasks.

## Usage

### With docker

Getting *sentimentator* up and running should be straightforward with Docker.
In your file system, navigate to the sentimentator directory. On the command line, build the Docker image:
    
    docker build -f Dockerfile -t sentimentator .

After building the image, run that image and expose port 5000. This example assumes your
image is called `sentimentator`. Run:

    docker run -d -p 5000:5000 sentimentator

to run a container, or:

    docker run -it --rm -p 5000:5000 -v $(pwd):/app --name sentimentator sentimentator
    
to run a container and use a shell inside the container. To use the shell, open another command line window and run:

    docker exec -it sentimentator <editor_name>

and navigate to localhost:5000 on a Web browser.

#### Demo data

Initially the database is empty. You can populate it with demo data by
executing the database initialization script in a running Docker container.
In a shell run:

    python3 data_import.py <lang_name> <lang_filename> <alignment_filename>

**<lang_name>**: two-letter language code, for example *en*, *fi*, or *sv*.

**<lang_filename>**: name of the .txt file from which to import each line as a sentence to the database.

**<alignment_filename>**: name of the .txt file from which to import the OPUS metadata for each sentence. The *data_import.py* script imports metadata for a pivot language by extracting the sentence id and the path to the OPUS document id for each sentence from the parallel line in the alignment file.
Example alignment file:

    # en/0/3509138/6031634.xml.gz	fi/0/3509138/6003289.xml.gz	5	3
    # en/0/3509138/6031634.xml.gz	fi/0/3509138/6003289.xml.gz	6	4
    # en/0/3509138/6031634.xml.gz	fi/0/3509138/6003289.xml.gz	9	6
    [...]
    
 For example, to import English, in a shell inside a running container run:

    python3 data_import.py en data/en/en.txt data/en/ids.txt

OPUS parallel corpus files are available for download at http://opus.nlpl.eu/OpenSubtitles2018.php in the MOSES/GIZA++ format.

The demo dataset used in this project is taken from the OPUS corpus as presented in this paper:
**P. Lison and J. Tiedemann, 2016, OpenSubtitles2016: Extracting Large Parallel Corpora from Movie and TV Subtitles. In Proceedings of the 10th International Conference on Language Resources and Evaluation (LREC 2016).**

The demo version of Sentimentator is located at http://sentimentator.it.helsinki.fi/

Please let us know if you use Sentimentator for your own project. We would love to know more about it! Use:
Öhman, E. and Kajava, K. 2018. Sentimentator: Gamifying Fine-grained Sentiment Annotation. In Digital Humanities
in the Nordic Countries 2018. CEUR Workshop Proceedings.
