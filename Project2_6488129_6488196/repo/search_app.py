from flask import Flask, request
from markupsafe import escape
from flask import render_template
from elasticsearch import Elasticsearch
import math

ELASTIC_PASSWORD = "sength123"

es = Elasticsearch("https://localhost:9200", http_auth=("elastic", ELASTIC_PASSWORD), verify_certs=False)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('search-song.html')

@app.route('/search')
def search():
    page_size = 10
    keyword = request.args.get('keyword')

    if request.args.get('page'):
        page_no = int(request.args.get('page'))
    else:
        page_no = 1

    body = {
        'size': page_size,
        'from': page_size * (page_no-1),
        'query': {
            'multi_match': {
                'query': keyword,
                'fields': ['name^5', 'author^4','releaseYear^4','album^4','lyrics^3'],
                'fuzziness': 'auto',
            }
        }
    }
    
    res = es.search(index='song-bulk', body=body)
    
    hits = [{'name': doc['_source']['name'], 'author': doc['_source']['author'], 'releaseYear': doc['_source']['releaseYear'], 'album': doc['_source']['album'], 'lyrics': doc['_source']['lyrics'], 'imageUrl': doc['_source']['imageUrl']} 
            for doc in res['hits']['hits']]
    page_total = math.ceil(res['hits']['total']['value']/page_size)
    return render_template('search.html',keyword=keyword, hits=hits, page_no=page_no, page_total=page_total)