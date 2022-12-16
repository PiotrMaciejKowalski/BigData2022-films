DIR="/content/drive/.shortcut-targets-by-id/1VcOir9FMG8LzEsUE-Q8YA79c_sV0tJwp/bigdata2022"
if [ -d "$DIR"];
then
    echo "downloading files into $DIR"
    wget "https://datasets.imdbws.com/name.basics.tsv.gz" -O $DIR/name.basics.tsv.gz
    wget "https://datasets.imdbws.com/title.akas.tsv.gz" -O $DIR/title.akas.tsv.gz
    wget "https://datasets.imdbws.com/title.basics.tsv.gz" -O $DIR/title.basics.tsv.gz
    wget "https://datasets.imdbws.com/title.crew.tsv.gz" -O $DIR/title.crew.tsv.gz
    wget "https://datasets.imdbws.com/title.episode.tsv.gz" -O $DIR/title.episode.tsv.gz
    wget "https://datasets.imdbws.com/title.principals.tsv.gz" -O $DIR/title.principals.tsv.gz
    wget "https://datasets.imdbws.com/title.ratings.tsv.gz" -O $DIR/title.ratings.tsv.gz
else
    echo "$DIR directory does not exist"
fi