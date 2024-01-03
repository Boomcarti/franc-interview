from flask import Flask, render_template, Response, request
from datetime import datetime
import json

app = Flask(__name__)

@app.route('/')
def index_view():
    with open('./users.json', 'r') as f:
        users = json.load(f)

    username = request.args.get('username')
    followlist = []

    if username and username in users:
        followlist = users[username]

    # Correctly read and parse posts.json
    with open('./posts.json', 'r') as f:
        posts = json.load(f)


    postlist = []       
    # Check if any of the followed users have posts
    for user in followlist:
        if user in posts:
            for post in posts[user]:
                post['time'] = datetime.strptime(post['time'], '%Y-%m-%dT%H:%M:%SZ')
                postlist.append(post)  # Append each post to postlist after adding the time object

    # Sort the posts by time in ascending order (new to Oldest)
    postlist.sort(key=lambda x: x['time'], reverse = True)

    return render_template('index.html', username=username, followlist=followlist, postlist=postlist)

@app.route('/users')
def users_view():
    with open('./users.json', 'r') as f:
        users = f.read()
    return Response(users, mimetype="application/json")

@app.route('/posts')
def posts_view():
    with open('./posts.json', 'r') as f:
        posts = f.read()
    return Response(posts, mimetype="application/json")

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug = True)