from flask import Flask, render_template, url_for, request
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=["http://127.0.0.1:9200"])


app = Flask(__name__)

MAX_SIZE = 10

@app.route("/home")
def dashboard():
    return render_template('dash.html')


@app.route("/search")
def auto_search():
    query = request.args['q'].lower()
    tokens = query.split(" ")
    print(tokens)

    clauses = [
        {
            "span_multi": {
                "match": {
                    "fuzzy": {
                        "Manufacturer": {
                            "value": i,
                            "fuzziness": "AUTO"
                        }
                    }
                }
            }
        } for i in tokens
    ]

    payload = {
        "bool": {
            "must": [
                {"span_near": {"clauses": clauses, "slop": 0, "in_order": False}}
            ]
        }
    }
    
    resp = es.search(index="laptops", body={"query": payload}, size=MAX_SIZE)
    return [result['_source']['Manufacturer'] for result in resp['hits']['hits']]



if __name__ == '__main__':
    app.run(debug=True)
