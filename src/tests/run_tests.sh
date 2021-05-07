#!/bin/zsh
echo "Running Tests"

# Download the card data used during tests
echo "Downloading test card data"

for l in `cat src/tests/data/test_queries.txt`; do
file=`echo $l | cut -d\| -f 1`;
query=`echo $l | cut -d\| -f 2`;
python src/scripts/query2file.py --query "$query" --output-file "src/tests/data/$file.json"
done;

python -m unittest -v src/tests/*.py