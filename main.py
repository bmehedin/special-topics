import json
from flask import Flask, render_template, request
from elastic_app_search import Client

app = Flask(__name__)

with open("config.json") as json_data_file:
    config = json.load(json_data_file)

client = Client(
    base_endpoint=config['appsearch']['base_endpoint'],
    api_key=config['appsearch']['api_key'],
    use_https=True
)

engine_name = config['appsearch']['engine_name']


@app.route("/")
def home():
   data = client.search(engine_name, "", {})
   return render_template("index.html", data=data)


@app.route("/search", methods=['POST'])
def search():
    if request.method == 'POST':
        query = request.form['search']
        data = client.search(engine_name, query)
        final = [[]]
        for d in data['results']:
            for round in d['rounds']['raw']:
                json_data = json.loads(round)
                match = json_data['matches'][0]
                team1 = match['team1']
                team2 = match['team2']
                date = match['date']
                score = match['score']['ft']
                if team2 == query or team1 == query:
                    final.append(f'On {date} the score between {team1} and {team2} was {score}')

        return render_template("index.html", data=final)


@app.route("/index")
def index():
    f = open('data.json',)
    documents = json.load(f)
    data = client.index_documents(engine_name, documents)
    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(port=8080, debug=True)
