import psycopg2
from flask import Flask, current_app, jsonify, request
from datetime import datetime

stories = [
    {
        "created_at": "Fri, 24 Jun 2022 17:25:16 GMT",
        "id": 1,
        "score": 42,
        "title": "Voters Overwhelmingly Back Community Broadband in Chicago and Denver",
        "updated_at": "Fri, 24 Jun 2022 17:25:16 GMT",
        "url": "https://www.vice.com/en/article/xgzxvz/voters-overwhelmingly-back-community-broadband-in-chicago-and-denver",
    },
    {
        "created_at": "Fri, 24 Jun 2022 17:25:16 GMT",
        "id": 2,
        "score": 23,
        "title": "eBird: A crowdsourced bird sighting database",
        "updated_at": "Fri, 24 Jun 2022 17:25:16 GMT",
        "url": "https://ebird.org/home",
    },
    {
        "created_at": "Fri, 24 Jun 2022 17:25:16 GMT",
        "id": 3,
        "score": 471,
        "title": "Karen Gillan teams up with Lena Headey and Michelle Yeoh in assassin thriller Gunpowder Milkshake",
        "updated_at": "Fri, 24 Jun 2022 17:25:16 GMT",
        "url": "https://www.empireonline.com/movies/news/gunpowder-milk-shake-lena-headey-karen-gillan-exclusive/",
    },
    {
        "created_at": "Fri, 24 Jun 2022 17:25:16 GMT",
        "id": 4,
        "score": 101,
        "title": "Pfizers coronavirus vaccine is more than 90 percent effective in first analysis, company reports",
        "updated_at": "Fri, 24 Jun 2022 17:25:16 GMT",
        "url": "https://www.cnbc.com/2020/11/09/covid-vaccine-pfizer-drug-is-more-than-90percent-effective-in-preventing-infection.html",
    },
    {
        "created_at": "Fri, 24 Jun 2022 17:25:16 GMT",
        "id": 5,
        "score": 87,
        "title": "Budget: Pensions to get boost as tax-free limit to rise",
        "updated_at": "Fri, 24 Jun 2022 17:25:16 GMT",
        "url": "https://www.bbc.co.uk/news/business-64949083",
    },
    {
        "created_at": "Fri, 24 Jun 2022 17:25:16 GMT",
        "id": 6,
        "score": 22,
        "title": "Ukraine war: Zelensky honours unarmed soldier filmed being shot",
        "updated_at": "Fri, 24 Jun 2022 17:25:16 GMT",
        "url": "https://www.bbc.co.uk/news/world-europe-64938934",
    },
    {
        "created_at": "Fri, 24 Jun 2022 17:25:16 GMT",
        "id": 7,
        "score": 313,
        "title": "Willow Project: US government approves Alaska oil and gas development",
        "updated_at": "Fri, 24 Jun 2022 17:25:16 GMT",
        "url": "https://www.bbc.co.uk/news/world-us-canada-64943603",
    },
    {
        "created_at": "Fri, 24 Jun 2022 17:25:16 GMT",
        "id": 8,
        "score": 2,
        "title": "SVB and Signature Bank: How bad is US banking crisis and what does it mean?",
        "updated_at": "Fri, 24 Jun 2022 17:25:16 GMT",
        "url": "https://www.bbc.co.uk/news/business-64951630",
    },
    {
        "created_at": "Fri, 24 Jun 2022 17:25:16 GMT",
        "id": 9,
        "score": 131,
        "title": "Aukus deal: Summit was projection of power and collaborative intent",
        "updated_at": "Fri, 24 Jun 2022 17:25:16 GMT",
        "url": "https://www.bbc.co.uk/news/uk-politics-64948535",
    },
    {
        "created_at": "Fri, 24 Jun 2022 17:25:16 GMT",
        "id": 10,
        "score": 41,
        "title": "Dancer whose barefoot video went viral meets Camilla",
        "updated_at": "Fri, 24 Jun 2022 17:25:16 GMT",
        "url": "https://www.bbc.co.uk/news/uk-england-birmingham-64953863",
    },
]

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


@app.route("/stories/<id>", methods=["PATCH"])
def update_story(id):
    data = request.json
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
