from flask import Flask, render_template, url_for, request, jsonify
from elasticsearch import Elasticsearch
from connect import connection

es = Elasticsearch(hosts=["http://127.0.0.1:9200"])

app = Flask(__name__)

MAX_SIZE = 30

@app.route("/home", methods=['GET', 'POST'])
def dashboard():
    con = connection()
    cur = con.cursor()
    search_query = request.args.get('search', ' ').strip()
    
    if search_query:
        # Use parameterized query to prevent SQL injection and get distinct job postings
        select_query = """
               WITH unique_jobs AS (
                   SELECT *, ROW_NUMBER() OVER (PARTITION BY position ORDER BY time_posted DESC) as rn
                   FROM jobs_listing
                   WHERE position = %s
               )
               SELECT * FROM unique_jobs WHERE rn = 1
           """        
        cur.execute(select_query, (search_query,))    
    else:
        # If no search query, select all distinct jobs
        select_query = "SELECT DISTINCT * FROM jobs_listing"
        cur.execute(select_query)

    jobs = cur.fetchall()
    cur.close()
    con.close()
    
    return render_template('dash.html', jobs=jobs)

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
                        "position": {
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
    unique_titles = {result['_source']['position'] for result in resp['hits']['hits']}
    
    # Convert the set to a list (optional, if you need to return a list)
    return list(unique_titles)

@app.route('/post_query', methods=['POST'])
def post_query():
    data = request.json
    query = data.get('query')
    # Process the query as needed
    return jsonify({"message": "Query received", "query": query})

if __name__ == '__main__':
    app.run(debug=True)
