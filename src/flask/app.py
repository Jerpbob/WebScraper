from flask import Flask, jsonify, request
from webscraper.webscrape import search_scraper, grab_chap_info

app = Flask(__name__)


# @app.route("/user/search", methods=["GET"])
# def search_result():
#     if request.method == "GET":
#         user_search = ss("Kaguya sama")
#         return jsonify(user_search)

@app.route("/user/search/<user_search>", methods=["GET"])
def search_result(user_search):
    if request.method == "GET":
        user_search_result = search_scraper(user_search)
        return jsonify(user_search_result)


@app.route("/user/manga/<manga_id>", methods=["GET"])
def manga_info(manga_id):
    if request.method == "GET":
        manga_info_result = grab_chap_info(manga_id)
        return jsonify(manga_info_result)


if __name__ == '__main__':
    app.run(debug=True)
