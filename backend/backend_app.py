from idlelib.macosx import hideTkConsole

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    if len(POSTS) == 0:
        return jsonify({
            "success": False,
            "message": "No posts yet"
        })

    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_posts():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    missing_fields = []

    if "title" not in data:
        missing_fields.append("title")
    if "content" not in data:
        missing_fields.append("content")

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing": missing_fields
        }), 400

    new_id = max(post["id"] for post in POSTS) + 1 if POSTS else 1

    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"]
    }

    POSTS.append(new_post)

    return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    global POSTS

    post_to_delete = None
    for post in POSTS:
        if post["id"] == id:
            post_to_delete = post
            break

    if post_to_delete is None:
        return jsonify({
            "error": f"Post with id {id} not found."
        }), 404

    POSTS.remove(post_to_delete)

    return jsonify({
        "message": f"Post with id {id} has been deleted successfully."
    }), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    data = request.get_json()

    post = None
    for p in POSTS:
        if p["id"] == id:
            post = p
            break

    if post is None:
        return jsonify({
            "error": f"Post with id {id} not found."
        }), 404

    if not data:
        return jsonify(post), 200

    if "title" in data:
        post["title"] = data["title"]

    if "content" in data:
        post["content"] = data["content"]

    return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get('title')
    content_query = request.args.get('content')

    results = POSTS

    if title_query:
        results = [
            post for post in results
            if title_query.lower() in post["title"].lower()
        ]

    if content_query:
        results = [
            post for post in results
            if content_query.lower() in post["content"].lower()
        ]

    return jsonify(results)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
