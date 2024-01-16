import json
from routes import display
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
        final_data = display(data, query)
        return render_template("index.html", data=final_data)


@app.route("/index")
def index():
    f = open('data.json',)
    documents = json.load(f)
    data = client.index_documents(engine_name, documents)
    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(port=8080, debug=True)
