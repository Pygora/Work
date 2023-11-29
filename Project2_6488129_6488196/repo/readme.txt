cd C:\Users\HP\Downloads\elasticsearch-8.11.1\bin
./elasticsearch

cd C:\Users\HP\Downloads\kibana-8.11.1\bin
./kibana

python elasticsearch_loader.py --file song-bulk.json --index index-test-upload

cd C:\Users\HP\Downloads\elasticsearch\repo
set FLASK_APP=search_app
flask run

http://127.0.0.1:5000/

love
Taylor Swift 
love you
