from re import search
import flask
import os
import requests
import json

app = flask.Flask(__name__)

search_history = []

@app.route("/")
def index():
    return flask.send_from_directory('./build',"index.html")
@app.route('/<path:path>')
def index_file(path):
    return flask.send_from_directory('./build',"index.html")
@app.route("/static/js/<path:path>")
def staticjs_file(path):
    return flask.send_from_directory('./build/static/js',path)
@app.route("/static/css/<path:path>")
def staticcss_file(path):
    return flask.send_from_directory('./build/static/css',path)
    
@app.route('/api/search', methods=['POST'])
def api_test():
    req_data = flask.request
    google_res = requests.get(f"https://www.googleapis.com/customsearch/v1?key={os.getenv('GOOGLE_API','')}&q={req_data.json['data']}&cx={os.getenv('GOOGLE_CX','')}&num=4&searchType=image&start=1")
    tmp_data = {}
    tmp_data['data'] = []
    for i in json.loads(google_res.content.decode("utf-8"))['items']:
        tmp_data.data.append({
            "title": i['title'],
            "imgurl": i['link'],
            "contexturl": i['image']['contextLink'],
            "thumbnail": {
                "url": i['image']['thumbnailLink'],
                "width": i['image']['thumbnailWidth'],
                "height": i['image']['thumbnailHeight']
            }
        })
    if(len(search_history) > 10):
        search_history.pop(len(search_history)-1)
        search_history.insert(0,req_data.json['data'])
    else:
        search_history.append(req_data.json['data'])
    tmp_data.history = search_history
    response = flask.make_response(json.dumps(tmp_data), 200)
    response.mimetype = 'application/json'
    return response
@app.route('/api/search/history', methods=['GET'])
def api_search_history():
    response = flask.make_response(json.dumps(search_history), 200)
    response.mimetype = 'application/json'
    return response


if __name__ == "__main__":
    app.run()

