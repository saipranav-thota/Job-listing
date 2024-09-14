from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route("/home")
def search_autocomplete():
    return render_template('dash.html')

# # Dummy data for the example
# data = ["apple", "banana", "orange", "grape", "pineapple", "watermelon"]

# @app.route('/home', methods=['GET'])
# def search():
#     query = request.args.get('query')
#     if query:
#         # Filter the data (you can replace this logic with database querying)
#         results = [item for item in data if query.lower() in item.lower()]
#     else:
#         results = []

#     return render_template('dash.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
