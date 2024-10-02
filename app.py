from flask import Flask, render_template, url_for, request
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=["http://127.0.0.1:9200"])

app = Flask(__name__)

MAX_SIZE = 30

@app.route("/home")
def dashboard():
    return render_template('dash.html')

@app.route("/search")
def auto_search():
    query = request.args.get('q', '').lower()  # Use get to handle missing params
    tokens = query.split(" ")
    print(tokens)

    clauses = [
        {
            "span_multi": {
                "match": {
                    "fuzzy": {
                        "title": {
                            "value": token,
                            "fuzziness": "AUTO"
                        }
                    }
                }
            } for token in tokens
        }
    ]

    payload = {
        "bool": {
            "must": [
                {"span_near": {"clauses": clauses, "slop": 0, "in_order": False}}
            ]
        }
    }
    
    resp = es.search(index="jobs_listing", body={"query": payload}, size=MAX_SIZE)
    
    # Use a set to collect unique titles
    unique_titles = {result['_source']['title'] for result in resp['hits']['hits']}
    
    # Convert the set to a list (optional, if you need to return a list)
    return list(unique_titles)

if __name__ == '__main__':
    app.run(debug=True)
