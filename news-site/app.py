import psycopg2
from flask import Flask, current_app, jsonify, request
from datetime import datetime
from json import load

f = open("stories.json")
stories = load(f)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return current_app.send_static_file("index.html")


@app.route("/add", methods=["GET"])
def addstory():
    return current_app.send_static_file("./addstory/index.html")


@app.route("/scrape", methods=["GET"])
def scrape():
    return current_app.send_static_file("./scrape/index.html")


@app.route("/stories", methods=["GET", "POST"])
def get_stories():
    if request.method == "GET":
        if len(stories) == 0:
            return jsonify({"error": True, "message": "No stories were found"}), 404
        args = request.args.to_dict()
        search = args.get("search")
        if search:
            searched_stories = [
                story for story in stories if search.lower() in story["title"].lower()
            ]
            return jsonify(searched_stories), 200
        sort = args.get("sort")
        if sort.lower() == "created":
            sort = "created_at"
        if sort.lower() == "modified":
            sort = "updated_at"
        if args.get("order") == "ascending":
            return jsonify(sorted(stories, key=lambda x: x[sort])), 200
        else:
            return jsonify(sorted(stories, key=lambda x: x[sort], reverse=True)), 200
    if request.method == "POST":
        data = request.json
        stories.append(
            {
                "created_at": datetime.now(),
                "id": len(stories) + 1,
                "score": 0,
                "title": data["title"],
                "updated_at": datetime.now(),
                "url": data["url"],
            }
        )
        return jsonify(stories), 200


@app.route("/stories/<id>", methods=["PATCH", "DELETE"])
def update_story(id):
    global stories
    if request.method == "PATCH":
        data = request.json
        updated_story = stories[int(id) - 1]
        updated_story["title"] = data["title"]
        updated_story["url"] = data["url"]
        updated_story["updated_at"] = datetime.now()

    if request.method == "DELETE":
        print(id)
        stories = [story for story in stories if story["id"] != int(id)]
    return jsonify(stories), 200


@app.route("/stories/<id>/votes", methods=["POST"])
def add_vote(id):
    if request.method == "POST":
        data = request.json
        print(data)
        for story in stories:
            if story["id"] == int(id):
                if data["direction"] == "up":
                    story["score"] += 1
                    story["updated_at"] = datetime.now()
                elif data["direction"] == "down":
                    if story["score"] == 0:
                        return jsonify(
                            {
                                "error": True,
                                "message": "Can't downvote for a story with a score of 0",
                            },
                            404,
                        )
                    story["score"] -= 1
                    story["updated_at"] = datetime.now()
    return jsonify(stories), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
