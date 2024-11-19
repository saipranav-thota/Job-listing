from flask import Flask, render_template, url_for, request, jsonify, redirect
from elasticsearch import Elasticsearch
from connect import connection

es = Elasticsearch(hosts=["http://127.0.0.1:9200"])

app = Flask(__name__)

MAX_SIZE = 30

@app.route("/home", methods=['GET', 'POST'])
def dashboard():
    con = connection()
    cur1 = con.cursor()
    
    # Get filter values from request
    search_query = request.args.get('search', '').strip()
    date_posted = request.args.get('Date Posted')
    experience = request.args.get('Experience')
    employment_type = request.args.get('Employment')
    work_mode = request.args.get('Work Mode')
    location = request.args.get('Location')

    # Handle experience as an integer (if valid) or set to None
    if experience and experience.isdigit():
        experience = int(experience)
    else:
        experience = None

    # Initialize base query
    query = "SELECT * FROM jobs_listing WHERE 1=1"  # 1=1 allows us to easily append conditions
    params = []

    # Add filters dynamically
    if date_posted:
        query += " AND date_posted = %s"
        params.append(date_posted)

    if experience is not None and 0 <= experience <= 30:
        query += " AND min_experience <= %s AND max_experience >= %s"
        params.append(experience)  # Add experience for min_experience
        params.append(experience)  # Add experience again for max_experience

    if employment_type:
        query += " AND employment_type = %s"
        params.append(employment_type)

    if work_mode:
        query += " AND work_mode = %s"
        params.append(work_mode)

    if location:
        query += " AND location = %s"
        params.append(location)

    # Debugging: Print final query and params to verify
    print("Final Query:", query)
    print("Params:", params)

    # Execute the query with parameters
    cur1.execute(query, params)

    # Fetch filtered results
    results = cur1.fetchall()
    cur1.close()

    # Handle search query for job position (if search is used)
    if search_query:
        cur2 = con.cursor()
        search_query = '%' + search_query + '%'  # Enable partial match using LIKE
        select_query = '''
            WITH unique_jobs AS (
                SELECT *, ROW_NUMBER() OVER (PARTITION BY position ORDER BY date_posted DESC) as rn
                FROM jobs_listing
                WHERE position LIKE %s
            )
            SELECT * FROM unique_jobs WHERE rn = 1
            '''
        cur2.execute(select_query, (search_query,))
        jobs = cur2.fetchall()
        cur2.close()
    else:
        # Use the filtered results if no search is used
        jobs = results if results else []

    # Close the connection
    con.close()

    # Return filtered jobs and results to the template
    return render_template('dash.html', jobs=jobs)

# results=results


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

@app.route('/job/<int:job_id>')
def get_job(job_id):
    con = connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute('SELECT * FROM jobs_listing WHERE id = %s', (job_id,))
    job = cursor.fetchone()
    cursor.close()
    con.close()
    return jsonify(job)

@app.route('/landing')
def landing():
    con = connection()
    search_query = request.args.get('search', '').strip()
    print(search_query)

    jobs = []  # Initialize jobs to an empty list

    # Handle search query for job position (if search is used)
    if search_query:
        cur2 = con.cursor()
        search_query = '%' + search_query + '%'  # Enable partial match using LIKE
        select_query = '''
            WITH unique_jobs AS (
                SELECT *, ROW_NUMBER() OVER (PARTITION BY position ORDER BY date_posted DESC) as rn
                FROM jobs_listing
                WHERE position LIKE %s
            )
            SELECT * FROM unique_jobs WHERE rn = 1
            '''
        cur2.execute(select_query, (search_query,))
        jobs = cur2.fetchall()
        cur2.close()
        return redirect(url_for('dashboard', search=search_query))

    # Close the connection
    con.close()

    # Return filtered jobs and results to the template
    return render_template('landing.html', jobs=jobs)

if __name__ == '__main__':
    app.run(debug=True)