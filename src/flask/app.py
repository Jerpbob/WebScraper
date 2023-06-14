from flask import Flask, jsonify, request
from webscraper.webscrape import search_scraper as ss

app = Flask(__name__)


# @app.route("/user/search", methods=["GET"])
# def search_result():
#     if request.method == "GET":
#         user_search = ss("Kaguya sama")
#         return jsonify(user_search)

@app.route("/user/search/<user_search>", methods=["GET"])
def search_result(user_search):
    if request.method == "GET":
        user_search_result = ss(user_search)
        return jsonify(user_search_result)


if __name__ == '__main__':
    app.run(debug=True)
