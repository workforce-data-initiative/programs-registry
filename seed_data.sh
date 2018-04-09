cd seed_data &&
unzip -d data/ data.zip &&
python seed_data.py &&
rm -rf data &&
cd ..
